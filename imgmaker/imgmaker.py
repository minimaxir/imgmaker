from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from jinja2 import Markup, Environment
from markdown import markdown
from base64 import b64encode
import io
import os
import logging
from pkg_resources import resource_filename
import yaml
from typing import List
import pngquant
import shutil

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class imgmaker:
    def __init__(
        self,
        chromedriver_path: str = "./chromedriver",
        scale: int = 2,
        add_args: List[str] = [],
    ):
        assert isinstance(scale, int), "scale must be an integer."
        self.scale = scale
        self.env = build_jinja_env()

        chrome_options = Options()

        args = [
            "--headless",
            "--hide-scrollbars",
            "--disable-gpu",
            f"--force-device-scale-factor={scale}",
        ] + add_args

        for arg in args:
            chrome_options.add_argument(arg)

        self.driver = webdriver.Chrome(
            executable_path=chromedriver_path, options=chrome_options
        )

    def generate(
        self,
        template_path: str = "hero",
        template_params: dict = {},
        width: int = None,
        height: int = None,
        downsample: bool = True,
        output_file: str = "img.png",
        save_html: bool = False,
        use_pngquant: bool = False,
    ):

        if use_pngquant:
            assert shutil.which("pngquant"), (
                "use_pngquant was set to True but pngquant is "
                + "not installed on the system."
            )

        if os.path.isfile(template_path):
            # if loading a template outside the package
            html = render_html_template(self.env, template_path, template_params)
            width = width or 512
        else:
            # if using an included template
            template_folder = resource_filename(__name__, "templates")
            template_subfolder = os.path.join(template_folder, template_path)
            assert os.path.isdir(
                template_subfolder
            ), f"{template_path} is not an included template with imgmaker."

            config_path = os.path.join(template_subfolder, "config.yaml")
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)

            full_path = os.path.join(template_subfolder, config["template"])
            params = config["default_params"]
            params.update(template_params)
            height = height or config["height"]
            width = width or config["width"]
            html = render_html_template(self.env, full_path, params)

        if save_html:
            with open("rendered_html.html", "w", encoding="utf-8") as f:
                f.write(html)

        self.driver.get(f"data:text/html;charset=utf-8,{html}")

        if height is None or height == -1:
            self.driver.set_window_size(width, 1)
            height = self.driver.find_element_by_tag_name("html").size["height"]

        self.driver.set_window_size(width, height)

        if self.scale > 1 and downsample:
            img = Image.open(io.BytesIO(self.driver.get_screenshot_as_png()))
            img = img.resize(
                (int(img.size[0] / self.scale), int(img.size[1] / self.scale)),
                Image.ANTIALIAS,
            )
            img.save(output_file)
        else:
            self.driver.get_screenshot_as_file(output_file)

        if use_pngquant:
            logger.info(f"Compressing {output_file} with pngquant.")
            pngquant.quant_image(output_file)

    def close(self):
        self.driver.close()


def build_jinja_env():
    # https://stackoverflow.com/q/15555870
    def safe_markdown(text: str):
        return Markup(markdown(text, extensions=["smarty"]))

    def strip_markdown(text: str):
        """
        Removes the <p> and </p> tags added by default.
        """
        return safe_markdown(text)[3:-4]

    def img_encode(img_path: str):
        """
        Checks if a provided image is a local image or a remote image.
        If local, encodes the image as a base64 string,
        required for local images to display in the Chromedriver.
        """
        # If the img_path is not provided as a parameter.
        if not img_path:
            return ""

        if os.path.isfile(img_path):
            # Local image
            with open(img_path, "rb") as f:
                img_str = str(b64encode(f.read()))[2:-1]
            img_type = img_path[-3:]
            img_str = f"data:image/{img_type};base64,{img_str}"
        else:
            # Remote image
            logging.info(f"Downloading {img_path}")
            img_str = img_path

        return img_str

    env = Environment()
    env.filters.update(
        {
            "markdown": strip_markdown,
            "markdown_nostrip": safe_markdown,
            "img_encode": img_encode,
        }
    )
    return env


def render_html_template(env: Environment, template_path: str, template_params: dict):
    with open(template_path, "r", encoding="utf-8") as f:
        html_template = env.from_string(f.read())
    return html_template.render(template_params)

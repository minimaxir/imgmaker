from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from jinja2 import Markup, Environment
from markdown import markdown
from base64 import b64encode
from sys import platform
import io
import os
import logging
import requests
import zipfile
import fire
from pkg_resources import resource_filename
import yaml
import psutil


class imgmaker:
    def __init__(self, chromedriver_path="./chromedriver", scale=2):
        assert isinstance(scale, int), "scale must be an integer."
        self.scale = scale
        self.env = build_jinja_env()

        chrome_options = Options()

        for arg in [
            "--headless",
            "--hide-scrollbars",
            "--disable-gpu",
            f"--force-device-scale-factor={scale}",
        ]:
            chrome_options.add_argument(arg)

        self.driver = webdriver.Chrome(
            executable_path=chromedriver_path, options=chrome_options
        )

    def generate(
        self,
        template_path="hero",
        template_params={},
        width=None,
        height=None,
        downsample=True,
        output_file="img.png",
        save_html=False,
    ):

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

    def close(self):
        self.driver.close()


def build_jinja_env():
    # https://stackoverflow.com/q/15555870
    def safe_markdown(text):
        return Markup(markdown(text, extensions=["smarty"]))

    def strip_markdown(text):
        """
        Removes the <p> and </p> tags added by default.
        """
        return safe_markdown(text)[3:-4]

    def img_encode(img_path):
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
            logging.info("Downloading {img_path}")
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


def render_html_template(env, template_path, template_params):
    with open(template_path, "r", encoding="utf-8") as f:
        html_template = env.from_string(f.read())
    return html_template.render(template_params)


def kill_all_chrome():
    # https://stackoverflow.com/a/4230226
    for proc in psutil.process_iter():
        name = proc.name()
        if name == "chromedriver" or name in "Google Chrome":
            proc.kill()
    print("All Chrome and chromedriver processes killed.")


def download_chromedriver():
    """
    Downloads the latest version of Chromedriver corresponding to the
    `stable` Chrome branch.
    """

    if os.path.isfile("chromedriver"):
        print("chromedriver binary is already present in the current directory.")
        return

    latest_chrome = requests.get(
        "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    ).text

    # https://stackoverflow.com/a/8220141
    platforms_binary = {
        "linux": "linux64",
        "darwin": "mac64",
        "win32": "win32",
    }

    binary = platforms_binary[platform]

    print(f"Downloading ChromeDriver {latest_chrome} for {binary}.")

    chromedriver = requests.get(
        f"https://chromedriver.storage.googleapis.com/{latest_chrome}/chromedriver_{binary}.zip",
        stream=True,
    )

    with open("chromedriver.zip", "wb") as f:
        for chunk in chromedriver.iter_content(chunk_size=128):
            f.write(chunk)

    # https://stackoverflow.com/a/46837272
    with zipfile.ZipFile("chromedriver.zip", "r") as zf:
        for info in zf.infolist():
            extracted_path = zf.extract(info, "")

            if info.create_system == 3:
                unix_attributes = info.external_attr >> 16
                if unix_attributes:
                    os.chmod(extracted_path, unix_attributes)

    os.remove("chromedriver.zip")


def imgmaker_cli(
    action="chromedriver",
    template_path="hero",
    template_params={},
    chromedriver_path="./chromedriver",
    scale=2,
    width=None,
    height=None,
    downsample=True,
    output_file="img.png",
):
    """Create high-quality images programmatically using easily-hackable templates.

    action: Action to perform. Select `chromedriver` to download Chromedriver,
    `generate` to generate an image.
    """

    assert action in [
        "chromedriver",
        "kill-all-chrome",
        "generate",
    ], "action must be chromedriver or generate."

    if action == "chromedriver":
        download_chromedriver()
    elif action == "kill-all-chrome":
        kill_all_chrome()
    elif action == "generate":
        i = imgmaker(chromedriver_path, scale)
        i.generate(
            template_path, template_params, width, height, downsample, output_file
        )
        i.close()


def imgmaker_cli_handler(**kwargs):
    fire.Fire(imgmaker_cli)

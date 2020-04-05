from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from jinja2 import Markup, Environment
from markdown import markdown
from base64 import b64encode
import io


class imgmaker:
    def __init__(self, chromedriver_path, scale=2):
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
        template_path,
        template_params,
        width=1024,
        height=None,
        downsample=True,
        output_file="img.png",
    ):
        html = render_html_template(self.env, template_path, template_params)

        # with open("test.html", "w") as f:
        #     f.write(html)

        self.driver.get(f"data:text/html;charset=utf-8,{html}")

        if height is None:
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
        if text is None:
            return None
        return safe_markdown(text)[3:-4]

    def img_encode(img_path):
        """
        Encodes a local image as a base64 string,
        required for local images to display in the Chromedriver.
        """
        with open(img_path, "rb") as f:
            img_str = str(b64encode(f.read()))[2:-1]
        img_type = img_path[-3:]
        img_str = f"data:image/{img_type};base64,{img_str}"
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


if __name__ == "__main__":
    c = imgmaker("/Users/maxwoolf/Downloads/chromedriver")
    # c.generate(
    #     "test_template.html",
    #     {
    #         "title": "I am a *big* pony!",
    #         "subtitle": 'It is "true!"',
    #         "color": "dark",
    #         "bold": True,
    #         "center": True,
    #         "custom_css": ":root {font-size: 200%;}",
    #     },
    #     width=800,
    #     height=450,
    # )

    c.generate(
        "meme.html",
        {
            "top_text": "Memes are Good",
            "bottom_text": "Yes they are!",
            "background": "ss.png",
            # "custom_css": ":root {font-size: 200%;}",
        },
        width=800,
        height=800,
        output_file="meme.png",
    )
    c.close()

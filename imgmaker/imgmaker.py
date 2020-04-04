from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import io


class imgmaker:
    def __init__(self, chromedriver_path, scale=2):
        assert isinstance(scale, int), "scale must be an integer."
        self.scale = scale

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
        self, url, width=1024, height=768, downsample=False, output_file="img.png"
    ):
        self.driver.get(url)
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


if __name__ == "__main__":
    c = imgmaker("/Users/maxwoolf/Downloads/chromedriver")
    c.generate("https://bulma.io/documentation/", downsample=False)
    c.close()

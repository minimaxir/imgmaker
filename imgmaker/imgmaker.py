from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import io

scale = 2
output_file = "test2x.png"

chrome_options = Options()

for arg in [
    "--headless",
    "--hide-scrollbars",
    "--disable-gpu",
    f"--force-device-scale-factor={scale}",
]:
    chrome_options.add_argument(arg)

driver = webdriver.Chrome(
    executable_path="/Users/maxwoolf/Downloads/chromedriver", options=chrome_options
)
driver.get("https://www.google.com")


if scale > 1:
    img = Image.open(io.BytesIO(driver.get_screenshot_as_png()))
    img = img.resize(
        (int(img.size[0] / scale), int(img.size[1] / scale)), Image.ANTIALIAS
    )
    img.save(output_file)
else:
    driver.get_screenshot_as_file(output_file)

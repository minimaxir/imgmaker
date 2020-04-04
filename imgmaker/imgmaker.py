from selenium import webdriver
from selenium.webdriver.chrome.options import Options

scale = 2

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
driver.get_screenshot_as_file("test.png")

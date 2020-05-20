import psutil
import os
import requests
import fire
import zipfile
from sys import platform
from .imgmaker import imgmaker


def imgmaker_cli():
    """
    Create high-quality images programmatically using easily-hackable templates.
    """

    fire.Fire(
        {
            "chromedriver": download_chromedriver,
            "kill-all-chrome": kill_all_chrome,
            "generate": generate,
        }
    )


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


def kill_all_chrome():
    """
    Kills all Chrome processes, in case there are orphaned processed
    from killed imgmaker instances that did not close.
    """

    # https://stackoverflow.com/a/4230226
    for proc in psutil.process_iter():
        name = proc.name()
        if name == "chromedriver" or name in "Google Chrome":
            proc.kill()
    print("All Chrome and chromedriver processes killed.")


def generate(
    template_path: str = "hero",
    template_params: dict = {},
    chromedriver_path: str = "./chromedriver",
    scale: int = 2,
    width: int = None,
    height: int = None,
    downsample: bool = True,
    output_file: str = "img.png",
    use_pngquant: bool = False,
):
    """
    Generates an image according to the
    given parameters.
    """
    i = imgmaker(chromedriver_path, scale)
    i.generate(
        template_path,
        template_params,
        width,
        height,
        downsample,
        output_file,
        use_pngquant=use_pngquant,
    )
    i.close()

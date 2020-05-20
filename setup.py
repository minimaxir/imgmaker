from setuptools import setup

long_description = """
Create high-quality images programmatically using easily-hackable templates.
"""


setup(
    name="imgmaker",
    packages=["imgmaker"],  # this must be the same as the name above
    version="0.2",
    description="Create high-quality images programmatically using easily-hackable templates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Max Woolf",
    author_email="max@minimaxir.com",
    url="https://github.com/minimaxir/imgmaker",
    keywords=["images", "image generation", "cool stuff"],
    classifiers=[],
    license="MIT",
    entry_points={"console_scripts": ["imgmaker=imgmaker.cli:imgmaker_cli"]},
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=[
        "selenium",
        "jinja2",
        "Pillow",
        "requests",
        "fire>=0.3.0",
        "markdown",
        "psutil",
        "pyyaml",
        "pngquant",
    ],
)

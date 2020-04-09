# imgmaker

![](https://github.com/minimaxir/imgmaker/blob/master/docs/img/meme3.png?raw=true)

Create high-quality images programmatically using easily-hackable templates.

imgmaker is a Python package that leverages headless [Google Chrome](https://www.google.com/chrome/) via [selenium](https://selenium-python.readthedocs.io) for image generation, which counterintuitively has many benefits:

- Renders images at Retina resolution (2x DPI) for improved image/text quality, and downsamples them by default for further improved antialiasing.
- Templates are just HTML and CSS, allowing them to be tweaked even by designers.
- Since the CSS is responsive, you get conditional image adjustments based on the image width without additional code flows.
- Optional dynamic image height to fit whatever text is provided.
- Leverages [jinja2](https://jinja.palletsprojects.com/en/2.11.x/) for Python templating, [Bulma](https://bulma.io) for high-quality CSS-only layouts, and [Font Awesome](https://fontawesome.com) for icon fonts.

The generated images can be used for many things, including social sharing thumbnails, Twitter bots, and APIs.

## Installation

imgmaker can be installed from PyPI via pip. (Python 3.6+)

```sh
pip3 install imgmaker
```

You will also need to download a [ChromeDriver](https://chromedriver.chromium.org) with the _same_ version as your installed Google Chrome. imgmaker has a CLI tool that will automatically download the ChromeDriver for your platform corresponding to the latest `stable` version to the current directory:

```sh
imgmaker chromedriver
```

## Maintainer/Creator

Max Woolf ([@minimaxir](https://minimaxir.com))

_Max's open-source projects are supported by his [Patreon](https://www.patreon.com/minimaxir) and [GitHub Sponsors](https://github.com/sponsors/minimaxir). If you found this project helpful, any monetary contributions to the Patreon are appreciated and will be put to good creative use._

# imgmaker

Create high-quality images programmatically with easily-hackable templates.

imgmaker is a Python package that counterintuitively leverages headless Google Chrome for image generation, which has many benefits:

- Renders images at Retina resolution (2x DPI), and downsamples them by default for improved antialiasing.
- Templates are just HTML and CSS, allowing them to be tweaked even by non-engineers.
- Since the CSS is responsive, you get conditional image adjustments based on the image width without additional code flows.
- Leverages jinja2 for Python templating, Bulma for high-quality CSS-only layouts, and Font Awesome for icon fonts.
- Markdown support for templates for improved styling.

## Installation

imgmaker can be installed via pip. (Python 3.6+)

```sh
pip3 install imgmaker
```

You will also need to download a Chromedriver with the _same_ version as your installed Google Chrome. imgmaker has a CLI tool that will automacally download the appropriate version to the current directory.

## Usage

First, you can instantiate an `imgmaker` object for generation, which starts up a headless Google Chrome in the background.

```python
i = imgmaker()
```

imgmaker contains built-in templates (you can view all the templates in the corresponding folder, with READMEs for each one)

## Helpful Notes

- Yes, using Google Chrome automation is a galaxy-brain approach toward programmatic image generation. However, the feature robustness of Chrome and hackability it allows far outweights the "weight" of Chrome, and it would take substantially more code to natively replicate.

## To-Do

- Add a Docker container + an app to deploy (e.g. to Cloud Run)

## Maintainer/Creator

Max Woolf ([@minimaxir](https://minimaxir.com))

_Max's open-source projects are supported by his [Patreon](https://www.patreon.com/minimaxir) and [GitHub Sponsors](https://github.com/sponsors/minimaxir). If you found this project helpful, any monetary contributions to the Patreon are appreciated and will be put to good creative use._

## License

MIT

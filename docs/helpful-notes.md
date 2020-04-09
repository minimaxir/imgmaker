## Cleanup

When you are done, it's recommended to close the Google Chrome instance, otherwise they will hang around:

```python
i.close()
```

...or you can take the thermonuclear option and kill _all_ chromedrivers and Chrome instances from the command line.

```
imgmaker kill-all-chrome
```

## Protips

- Yes, using Google Chrome automation is a galaxy-brain approach toward programmatic image generation. However, the feature robustness of Chrome and hackability it allows far outweights the "weight" of Chrome, and it would take substantially more code to natively replicate, especially cross-platform.
- If you want to intentionally create Retina (2x DPI) or higher assets, you can disable downsampling by passing `downsampling=False` to `generate()`. Additionally, you can pass a `scale` value to the `imgmaker()` constructor (e.g. `imgmaker(scale=6)`) for _very_ high-resolution pictures!
- Do not use `custom_css` with id-level rules; this causes the ChromeDriver to hang for whatever reason.

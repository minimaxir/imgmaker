A template invoking a variant of watermarking popular on social sharing cards. (although your mileage may vary)

## Template Dimensions

1280px x 640px

## Template Parameters

| Name         | Description   | Default                                              |
| ------------ | ------------- | ---------------------------------------------------- |
| `lang_icon`  | Language icon | `"fab fa-python"`                                    |
| `language`   | Language text | `"Python`                                            |
| `tags`       | Tag text      | `"image generation, APIs"`                           |
| `madeby`     | Author        | `"Made by me!"`                                      |
| `avatar`     | User avatar.  | [Mona Lisa](https://en.wikipedia.org/wiki/Mona_Lisa) |
| `background` | Background    | [Mona Lisa](https://en.wikipedia.org/wiki/Mona_Lisa) |

## Example Usage

(note: due to file-size [about 500KB per image], the images included on this page have been compressed using [TinyPNG](https://tinypng.com))

Set up imgmaker:

```python
from imgmaker import imgmaker

i = imgmaker()
```

No configuration:

```python
i.generate("github-social")
```

![](img/github-social1.png)

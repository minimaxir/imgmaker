import os
from PIL import Image

from imgmaker import imgmaker

if not os.path.exists("outputs"):
    os.makedirs("outputs")

# Update with the path to your chromedriver
i = imgmaker(chromedriver_path='/usr/local/bin/chromedriver')

# Basic test
output_file_1 = "outputs/test_img_1.png"
i.generate(output_file=output_file_1)
assert os.path.isfile(output_file_1), f"Test 1 Failed: {output_file_1} was not created."
print(f"Test 1 Passed: {output_file_1} created successfully.")

# Dimensions test
output_file_2 = "outputs/test_img_2.png"
i.generate(
    "hero",
    {"title": "imgmaker",
     "subtitle": "Create square images!"
    },
    width=512,
    height=512,
    output_file=output_file_2
)
assert os.path.isfile(output_file_2), f"Test 2 Failed: {output_file_2} was not created."
with Image.open(output_file_2) as img:
    width, height = img.size
    assert width == height, f"Test 2 Failed: Image dimensions are not square. Width: {width}, Height: {height}"
print(f"Test 2 Passed: {output_file_2} created successfully.")

# Style test
output_file_3 = "outputs/test_img_3.png"
i.generate(
    "hero",
    {
        "title": "imgmaker",
        "subtitle": "Create high-quality images programmatically.<br /><br />" +
                    "The generated images can be used for many things, " +
                    "including social sharing thumbnails, Twitter bots, and APIs.",
        "color": "dark",
        "bold": True,
        "custom_css": ".container {font-family: Comic Sans MS; transform: rotate(-20deg);}"
    },
    height=400,
    output_file=output_file_3
)
assert os.path.isfile(output_file_3), f"Test 3 Failed: {output_file_3} was not created."
print(f"Test 3 Passed: {output_file_3} created successfully.")

i.close()

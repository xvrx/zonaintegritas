from PIL import Image
from io import BytesIO


def captchaAdjust(png, location, size):
    im = Image.open(BytesIO(png))  # uses PIL library to open image in memory

    left = location["x"]
    top = location["y"]
    right = location["x"] + size["width"]
    bottom = location["y"] + size["height"]

    im = im.crop((left, top, right, bottom))  # defines crop points
    im.save("captch.png")  # saves new cropped image

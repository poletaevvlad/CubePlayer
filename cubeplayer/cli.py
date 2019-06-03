from argparse import ArgumentTypeError

from PIL import Image


def integer_type(min_value: int):
    def type(value: str):
        try:
            val = int(value)
            if val < min_value:
                raise ArgumentTypeError(f"the minimum value is {min_value}")
            return val
        except ValueError:
            raise ArgumentTypeError(f"invalid int value: '{value}'")
    return type


def duration_type(value: str):
    multiplier = 1
    if value.endswith("ms"):
        multiplier = 0.001
        value = value[:-2]
    elif value.endswith("s"):
        value = value[:-1]
    try:
        val = float(value)
        if val < 0:
            raise ArgumentTypeError("duration cannot be a negative number")
        return val * multiplier
    except ValueError:
        raise ArgumentTypeError(f"invalid number: '{value}'")


def texture_image(value: str):
    image = Image.open(value).convert("RGBA")
    image.thumbnail((512, 512))

    size = max(image.size)
    s = 2
    while s < size:
        s <<= 1

    scale = size / float(s)
    result = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    result.paste(image, ((s - image.size[0]) // 2, (s - image.size[1]) // 2))
    result.save("/home/vlad/tex.png")
    return result, scale


def dict_type(dictionary):
    def type(value: str):
        try:
            return dictionary[value]
        except KeyError:
            keys = list(dictionary.keys())
            options = ", ".join(keys[:-1]) + " or " + keys[-1]
            raise ArgumentTypeError(f"unknown value: `{value}`; expected either {options}")
    return type

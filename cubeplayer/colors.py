from argparse import ArgumentParser, ArgumentError, Namespace
from typing import Tuple, Dict
from libcube.cli.options import dict_type
from libcube.orientation import Color


def int_color(color):
    return (((color >> 16) & 0xFF) / 255.0, ((color >> 8) & 0xFF) / 255.0,
            (color & 0xFF) / 255.0)


ColorType = Tuple[float, float, float]

BACKGROUND_THEMES = {
    "grays": [(0.4, 0.4, 0.4), (0.2, 0.2, 0.2)],
    "white": [(1.0, 1.0, 1.0), (1.0, 1.0, 1.0)],
    "black": [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0)],
}

THEMES = {
    "default": {
        Color.WHITE: int_color(0xF4F4F4),
        Color.RED: int_color(0xF03939),
        Color.BLUE: int_color(0x5486D0),
        Color.ORANGE: int_color(0xEFA30F),
        Color.GREEN: int_color(0x6CBF39),
        Color.YELLOW: int_color(0xF3E139)
    },
    "gray": {
        Color.WHITE: int_color(0x404040),
        Color.RED: int_color(0x404040),
        Color.BLUE: int_color(0x404040),
        Color.ORANGE: int_color(0x404040),
        Color.GREEN: int_color(0x404040),
        Color.YELLOW: int_color(0x404040)
    }
}

COLOR_OPTIONS = {
    "red": Color.RED, "green": Color.GREEN, "orange": Color.ORANGE,
    "blue": Color.BLUE, "white": Color.WHITE, "yellow": Color.YELLOW
}


def color_type(value: str):
    if len(value) == 6:
        try:
            val = int(value, 16)
            return ((val >> 16) & 0xFF) / 255, ((val >> 8) & 0xFF) / 255, \
                   (val & 0xFF) / 255
        except ValueError:
            pass
    raise ArgumentError("the color must be a six digit hexadecimal RGB value")


def init_args_parser(args: ArgumentParser):
    colors_group = args.add_argument_group("color options")
    bg_group = colors_group.add_mutually_exclusive_group()
    bg_group.add_argument("--bg-theme", type=dict_type(BACKGROUND_THEMES),
                          help="background color theme", dest="bg_theme",
                          metavar="THEME", default=BACKGROUND_THEMES["grays"])
    bg_group.add_argument("--bg-colors", type=color_type, nargs=2, metavar="CLR",
                          help="colors for the background", dest="bg_colors")

    colors_group.add_argument("--theme", type=dict_type(THEMES), metavar="THEME",
                              help="cube stickers color theme", dest="cube_theme",
                              default=THEMES["default"])
    for color in COLOR_OPTIONS:
        colors_group.add_argument("--color-" + color, type=color_type, metavar="CLR",
                                  help=f"color of the {color} sticker",
                                  dest="color_" + color)


def get_background_theme(args: Namespace) -> Tuple[ColorType, ColorType]:
    if args.bg_colors is None:
        return tuple(args.bg_theme)
    else:
        return tuple(args.bg_colors)


def get_cube_colors(args: Namespace) -> Dict[Color, ColorType]:
    colors = args.cube_theme
    for name, color in COLOR_OPTIONS.items():
        value = getattr(args, "color_" + name)
        if value is not None:
            colors[color] = value
    return colors

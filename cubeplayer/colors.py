from argparse import ArgumentParser, ArgumentError, Namespace
from typing import Tuple
from libcube.cli.options import dict_type

ColorType = Tuple[float, float, float]

BACKGROUND_THEMES = {
    "grays": [(0.4, 0.4, 0.4), (0.2, 0.2, 0.2)],
    "white": [(1.0, 1.0, 1.0), (1.0, 1.0, 1.0)],
    "black": [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0)],
}


def color_type(value:str):
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


def get_background_theme(args: Namespace) -> Tuple[ColorType, ColorType]:
    if args.bg_colors is None:
        return tuple(args.bg_theme)
    else:
        return tuple(args.bg_colors)

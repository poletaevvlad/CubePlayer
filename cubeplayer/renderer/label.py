from argparse import ArgumentParser, Namespace
from typing import Optional

from OpenGL.GL import *

from cubelang.cube import Cube
from cubelang.orientation import Side, Orientation
from .engine.texture import Texture
from ..cli import texture_image, dict_type


class Label:
    def __init__(self, scale: float, texture: Texture, side: Side,
                 row: int, column: int):
        self.scale = scale
        self.texture = texture

        self.side = side
        self.row = row
        self.column = column

    ARG_SIDE = dict(front=Side.FRONT, back=Side.BACK, left=Side.LEFT,
                    right=Side.RIGHT, top=Side.TOP, bottom=Side.BOTTOM)

    @staticmethod
    def init_args_parser(arg_parser: ArgumentParser):
        group = arg_parser.add_argument_group("label options")
        group.add_argument("--label", metavar="PATH", dest="label_data",
                           help="path to a label file", type=texture_image)
        group.add_argument("--label-side", type=dict_type(Label.ARG_SIDE),
                           help="cube's side with a label", dest="label_side",
                           metavar="SIDE")
        group.add_argument("--label-position", metavar="I", type=int, nargs=2,
                           dest="label_position",
                           help="index of row and column of the labeled component")

    @staticmethod
    def from_arguments(args: Namespace, cube: Cube, parser: ArgumentParser) -> Optional["Label"]:
        if args.label_data is None:
            return None

        image, scale = args.label_data
        texture = Texture(image, GL_RGBA, flip=True, mipmap=True)
        if args.label_side is not None:
            side = args.label_side
        else:
            side = Side.TOP

        face = cube.get_side(Orientation.regular(side))
        if args.label_position is not None:
            i, j = args.label_position
            if i < 0 or i >= face.rows:
                parser.error(f"invalid label row: it must be between 0 and {face.rows - 1}")
                return None
            if j < 0 or j >= face.columns:
                parser.error(f"invalid label column: it must be between 0 and {face.columns - 1}")
                return None
        else:
            i = face.rows // 2
            j = face.columns // 2

        return Label(scale, texture, side, i, j)

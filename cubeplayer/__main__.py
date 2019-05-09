from libcube.actions import Action
from libcube.parser import get_action_representation
from libcube.cube import Cube
from libcube.orientation import Orientation, Color
from cubeplayer.parsing import CubeFormulaParamType, SideConfigurationType
from cubeplayer.glut_backend import GlutWindow

from typing import List, Tuple, Optional

import click
from click.exceptions import  BadOptionUsage
import signal


def apply_side(cube: Cube, orientation: Orientation,
               colors: Optional[List[List[Color]]], option_name: str):
    if colors is None:
        return
    side = cube.get_side(orientation)
    if side.rows != len(colors):
        raise BadOptionUsage(option_name, "Incorrect number of lines")
    elif side.columns != len(colors[0]):
        raise BadOptionUsage(option_name, "Incorrect number of columns")

    for i, line in enumerate(colors):
        for j, color in enumerate(line):
            side.colors[i, j] = color


@click.command()
@click.argument("formula", type=CubeFormulaParamType(), default="")
@click.option("-d", "--dim", nargs=3, type=click.types.IntRange(2), default=(3, 3, 3))
@click.option("-s", "--shuffle", type=CubeFormulaParamType(), default=[])
@click.option("--front", type=SideConfigurationType(), default=None)
@click.option("--left", type=SideConfigurationType(), default=None)
@click.option("--top", type=SideConfigurationType(), default=None)
@click.option("--right", type=SideConfigurationType(), default=None)
@click.option("--bottom", type=SideConfigurationType(), default=None)
@click.option("--back", type=SideConfigurationType(), default=None)
def main(formula: List[Action], dim: Tuple[int, int, int], shuffle: List[Action],
         front, left, top, right, bottom, back) -> None:
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    cube = Cube(dim)

    orientation = Orientation()
    apply_side(cube, orientation, front, "front")
    apply_side(cube, orientation.to_right, right, "right")
    apply_side(cube, orientation.to_left, left, "left")
    apply_side(cube, orientation.to_right.to_right, back, "back")
    apply_side(cube, orientation.to_top, top, "top")
    apply_side(cube, orientation.to_bottom, bottom, "bottom")

    for shuffle_action in shuffle:
        orientation = shuffle_action.perform(cube, orientation)

    window = GlutWindow(cube, list(map(get_action_representation, formula)))
    for action in formula:
        window.cube_animator.enqueue(action)
    window.run()


if __name__ == "__main__":
    # noinspection PyArgumentList
    main()

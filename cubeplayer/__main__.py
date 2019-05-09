from libcube.actions import Action
from libcube.parser import get_action_representation
from libcube.cube import Cube
from libcube.orientation import Orientation
from cubeplayer.parsing import CubeFormulaParamType
from cubeplayer.glut_backend import GlutWindow

from typing import List, Tuple

import click
import signal


@click.command()
@click.argument("formula", type=CubeFormulaParamType(), default="")
@click.option("-d", "--dim", nargs=3, type=click.types.IntRange(2), default=(3, 3, 3))
@click.option("-s", "--shuffle", type=CubeFormulaParamType(), default=[])
def main(formula: List[Action], dim: Tuple[int, int, int], shuffle: List[Action]) -> None:
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    cube = Cube(dim)
    orientation = Orientation()
    for shuffle_action in shuffle:
        orientation = shuffle_action.perform(cube, orientation)

    window = GlutWindow(cube, list(map(get_action_representation, formula)))
    for action in formula:
        window.cube_animator.enqueue(action)
    window.run()


if __name__ == "__main__":
    # noinspection PyArgumentList
    main()

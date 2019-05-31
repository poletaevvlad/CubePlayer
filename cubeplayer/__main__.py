import signal
from typing import List, Tuple

import click

from cubeplayer.glut_backend import GlutWindow
from libcube.actions import Action
from libcube.cli.entry import init_cube
from libcube.cli.options import CubeFormulaParamType, SideConfigurationType
from libcube.cube import Cube
from libcube.parser import get_action_representation


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
    init_cube(cube, shuffle, front, left, top, right, bottom, back)

    window = GlutWindow(cube, list(map(get_action_representation, formula)))
    for action in formula:
        window.cube_animator.enqueue(action)
    window.run()


if __name__ == "__main__":
    # noinspection PyArgumentList
    main()

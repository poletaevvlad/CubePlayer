from libcube.actions import Action
from libcube.cube import Cube
from cubeplayer.parsing import CubeFormulaParamType
from cubeplayer.glut_backend import GlutWindow

from typing import List

import click
import signal


@click.command()
@click.argument("formula", type=CubeFormulaParamType(), default="")
def main(formula: List[Action]) -> None:
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    window = GlutWindow(Cube((6, 6, 6)))
    for action in formula:
        window.cube_animator.enqueue(action)
    window.run()


if __name__ == "__main__":
    # noinspection PyArgumentList
    main()

from libcube.actions import Action
from cubeplayer.parsing import CubeFormulaParamType
from cubeplayer.renderer.scene import Scene

from typing import List

import click
from OpenGL.GLUT import *


def display(scene: Scene):
    width = glutGet(GLUT_WINDOW_WIDTH)
    height = glutGet(GLUT_WINDOW_HEIGHT)

    scene.render(width, height)
    glutSwapBuffers()
    glutPostRedisplay()


def run_glut():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_3_2_CORE_PROFILE)
    glutInitContextVersion(3, 3)
    glutInitContextProfile(GLUT_CORE_PROFILE)
    glutInitWindowSize(640, 480)
    glutCreateWindow("CubePlayer")


    scene = Scene()
    glutDisplayFunc(lambda: display(scene))
    glutMainLoop()


@click.command()
@click.argument("formula", type=CubeFormulaParamType(), default="")
def main(formula: List[Action]) -> None:
    run_glut()


if __name__ == "__main__":
    # noinspection PyArgumentList
    main()

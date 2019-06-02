from argparse import Namespace
from typing import List
from abc import ABC, abstractmethod
from OpenGL.GLUT import *
from OpenGL.GL import *

from libcube.cube import Cube
from libcube.orientation import Orientation
from .renderer import Scene
from .renderer.animation import Animator
from .renderer.cube_animation import CubeAnimationManager as CubeAnimator, WaitAction


class RenderingBackend(ABC):
    def __init__(self, cube: Cube, orientation: Orientation, args: Namespace,
                 formula: List[str]):
        self.args = args
        self.cube = cube
        self.orientation = orientation
        self.formula = formula

        self.init_gl()

        self.scene = Scene(self.cube, self.formula)
        self.animator = Animator()
        self.cube_animator = CubeAnimator(self.scene.cube, self.orientation,
                                          self.animator, self.scene.camera,
                                          self.scene.update_ui_position)

        if self.args.time_before > 0:
            self.cube_animator.enqueue(WaitAction(self.args.time_before / 1000))
        for action in self.args.formula:
            self.cube_animator.enqueue(action)
        if self.args.time_after > 0:
            self.cube_animator.enqueue(WaitAction(self.args.time_after / 1000))

    def create_glut_window(self, window_name: str, double_buffered: bool):
        glutInit(sys.argv)

        mode = GLUT_RGB | GLUT_DEPTH | GLUT_3_2_CORE_PROFILE
        if double_buffered:
            mode |= GLUT_DOUBLE
        if self.args.msaa > 1:
            mode |= GLUT_MULTISAMPLE
            glutSetOption(GLUT_MULTISAMPLE, self.args.msaa)

        glutInitDisplayMode(mode)
        glutInitContextVersion(3, 3)
        glutInitContextProfile(GLUT_CORE_PROFILE)
        glutInitWindowSize(*self.args.resolution)
        glutCreateWindow(window_name)

        if self.args.msaa > 1:
            glEnable(GL_MULTISAMPLE)

    @abstractmethod
    def init_gl(self):
        pass

    def run(self):
        pass

from argparse import Namespace, ArgumentParser
from typing import List, Optional
from abc import ABC, abstractmethod
from OpenGL.GLUT import *
from OpenGL.GL import *

from libcube.cube import Cube
from libcube.orientation import Orientation
from .renderer.label import Label
from .renderer import Scene
from .renderer.animation import Animator
from .renderer.cube_animation import CubeAnimationManager as CubeAnimator, WaitAction


class RenderingBackend(ABC):
    def __init__(self, cube: Cube, orientation: Orientation, args: Namespace,
                 formula: List[str], arg_parser: ArgumentParser):
        self.args = args
        self.cube = cube
        self.orientation = orientation
        self.formula = formula
        self.init_gl()

        label = Label.from_arguments(self.args, self.cube, arg_parser)
        self.scene = Scene(self.cube, self.formula, label)
        self.animator = Animator()
        self.cube_animator = CubeAnimator(self.scene.cube, self.orientation,
                                          self.animator, self.scene.camera,
                                          self.scene.update_ui_position)

        self._init_durations(self.cube_animator.turn_duration,
                             self.args.time_turn1, self.args.time_turn2)
        self._init_durations(self.cube_animator.rotation_duration,
                             self.args.time_rotation1, self.args.time_rotation1)

        if self.args.time_before > 0:
            self.cube_animator.enqueue(WaitAction(self.args.time_before))
        for action in self.args.formula:
            self.cube_animator.enqueue(action)
        if self.args.time_after > 0:
            self.cube_animator.enqueue(WaitAction(self.args.time_after))

    @staticmethod
    def _init_durations(values: List[float],
                        single: Optional[float], double: Optional[float]):
        if single is not None:
            values[0] = single
        if double is not None:
            values[1] = double

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

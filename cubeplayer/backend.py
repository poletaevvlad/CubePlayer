from argparse import Namespace
from typing import List
from abc import ABC, abstractmethod

from libcube.cube import Cube
from libcube.orientation import Orientation
from .renderer import Scene
from .renderer.animation import Animator
from .renderer.cube_animation import CubeAnimationManager as CubeAnimator


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

        for action in self.args.formula:
            self.cube_animator.enqueue(action)

    @abstractmethod
    def init_gl(self):
        pass

    def run(self):
        pass

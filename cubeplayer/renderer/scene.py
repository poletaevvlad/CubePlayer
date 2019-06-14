from typing import List, Optional, Tuple, Dict

from OpenGL.GL import *

from libcube.cube import Cube as CubeModel
from libcube.orientation import Color
from .label import Label
from .formula_ui import FormulaUI
from .cube import Cube, CubePart
from .engine.camera import Camera
from .engine.objects import Background

ColorType = Tuple[float, float, float]


class Scene:
    def __init__(self, cube: CubeModel[CubePart], factor: float,
                 rotation: List[float],
                 formula: List[str], ui_scale: float,
                 label: Optional[Label],
                 bg_colors: Tuple[ColorType, ColorType],
                 color_theme: Dict[Color, Tuple[float, float, float]]):
        self.camera = Camera(scale=factor * 5 / max(cube.shape))
        self.camera.rotation = rotation

        self.background: Background = Background(*bg_colors)
        self.cube = Cube(cube, label, color_theme)
        self.ui = FormulaUI(formula, ui_scale) if len(formula) > 0 else None

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def render(self, width: int, height: int) -> None:
        glDisable(GL_DEPTH_TEST)
        self.background.draw()

        glClear(GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        camera_transform = self.camera.position_transform().to_ctypes()
        camera_perspective = self.camera.perspective_transform(width, height).to_ctypes()
        self.cube.draw(camera_transform, camera_perspective)

        if self.ui is not None:
            glDisable(GL_DEPTH_TEST)
            self.ui.render(width, height)

    def rotate(self, delta_x: float, delta_y: float) -> None:
        self.camera.rotation[1] -= delta_x * 0.01
        self.camera.rotation[0] -= delta_y * 0.01

    def update_ui_position(self, position):
        if self.ui is not None:
            self.ui.position = position

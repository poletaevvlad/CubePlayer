from OpenGL.GL import *

from libcube.cube import Cube as CubeModel
from .formula_ui import FormulaUI
from .cube import Cube, CubePart
from .engine.camera import Camera
from .engine.objects import Background


class Scene:
    def __init__(self, cube: CubeModel[CubePart]):
        self.camera = Camera(scale=5 / max(cube.shape))
        self.camera.rotation = [-0.3, 0.5, 0]

        self.background: Background = Background((0.4, 0.4, 0.4), (0.2, 0.2, 0.2))
        self.cube = Cube(cube)
        self.ui = FormulaUI("Hello_world")

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

        self.ui.render(width, height)

    def rotate(self, delta_x: float, delta_y: float) -> None:
        self.camera.rotation[1] -= delta_x * 0.01
        self.camera.rotation[0] -= delta_y * 0.01

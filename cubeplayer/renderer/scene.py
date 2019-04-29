from OpenGL.GL import *

from .cube import Cube, CubePart
from .engine.camera import Camera
from .engine.objects import Background
from libcube.cube import Cube as CubeModel


class Scene:
    def __init__(self, cube: CubeModel[CubePart]):
        self.camera = Camera(scale=5 / max(cube.shape))
        self.camera.rotation = [-0.3, 0.5, 0]

        self.background: Background = Background((0.4, 0.4, 0.4), (0.2, 0.2, 0.2))
        self.cube = Cube(cube)

    def render(self, width: int, height: int) -> None:
        glDisable(GL_DEPTH_TEST)
        self.background.draw()

        glClear(GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        camera_transform = self.camera.position_transform().to_ctypes()
        camera_perspective = self.camera.perspective_transform(width, height).to_ctypes()
        self.cube.draw(camera_transform, camera_perspective)

    def rotate(self, delta_x: float, delta_y: float) -> None:
        self.camera.rotation[1] -= delta_x * 0.01
        self.camera.rotation[0] -= delta_y * 0.01

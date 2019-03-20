from OpenGL.GL import *

from .cube import Cube
from .engine.camera import Camera
from .engine.objects import Background


class Scene:
    def __init__(self):
        self.camera = Camera()
        self.camera.rotation = [-0.3, 0.5, 0]

        self.background: Background = Background((0.4, 0.4, 0.4), (0.2, 0.2, 0.2))
        self.cube = Cube((5, 5, 5))

    def render(self, width: int, height: int) -> None:
        glDisable(GL_DEPTH_TEST)
        self.background.draw()

        glEnable(GL_DEPTH_TEST)
        glClear(GL_DEPTH_BUFFER_BIT)

        camera_transform = self.camera.position_transform().to_ctypes()
        camera_perspective = self.camera.perspective_transform(width, height).to_ctypes()
        self.cube.draw(camera_transform, camera_perspective)

    def rotate(self, delta_x: float, delta_y: float) -> None:
        self.camera.rotation[1] -= delta_x * 0.01
        self.camera.rotation[0] -= delta_y * 0.01

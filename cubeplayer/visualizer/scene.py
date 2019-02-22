from OpenGL.GL import *

from .camera import Camera
from .objects import Background, CubeComponent


class Scene:
    def __init__(self):
        self.camera = Camera()
        self.background: Background = Background((0.2, 0.2, 0.2), (0.5, 0.5, 0.5))
        self.object = CubeComponent()

    def render(self, width: int, height: int) -> None:
        glClear(GL_DEPTH_BUFFER_BIT)
        self.background.draw()

        camera_transform = self.camera.transform(width, height).to_ctypes()
        self.object.draw(camera_transform)

from OpenGL.GL import *

from .animation import Animator
from .camera import Camera
from .objects import Background, CubeComponent


class Scene:
    def __init__(self):
        self.camera = Camera()
        self.animator = Animator()

        self.background: Background = Background((0.2, 0.2, 0.2), (0.5, 0.5, 0.5))
        self.object = CubeComponent()

    def rotate_camera(self, x: float):
        self.camera.rotation[2] = x

    def render(self, width: int, height: int, delta_time: float) -> None:
        self.animator.run(delta_time)

        self.background.draw()
        glClear(GL_DEPTH_BUFFER_BIT)

        camera_transform = self.camera.position_transform().to_ctypes()
        camera_perspective = self.camera.perspective_transform(width, height).to_ctypes()
        self.object.draw(camera_transform, camera_perspective)

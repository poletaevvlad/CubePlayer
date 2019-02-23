from OpenGL.GL import *

from .animation import Animator
from .engine.camera import Camera
from .engine.objects import Background
from .cube import Cube


class Scene:
    def __init__(self):
        self.camera = Camera()
        self.animator = Animator()

        self.background: Background = Background((0.2, 0.2, 0.2), (0.5, 0.5, 0.5))
        self.cube = Cube((5, 5, 5))

    def render(self, width: int, height: int, delta_time: float) -> None:
        glDisable(GL_DEPTH_TEST)
        self.background.draw()

        self.camera.rotation[1] += delta_time
        self.camera.rotation[0] += delta_time
        self.camera.rotation[2] += delta_time

        glEnable(GL_DEPTH_TEST)
        glClear(GL_DEPTH_BUFFER_BIT)
        self.animator.run(delta_time)

        camera_transform = self.camera.position_transform().to_ctypes()
        camera_perspective = self.camera.perspective_transform(width, height).to_ctypes()
        self.cube.draw(camera_transform, camera_perspective)

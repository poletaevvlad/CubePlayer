from OpenGL.GL import *

from .animation import Animator
from .engine.camera import Camera
from .engine.objects import Background
from .cube import Cube


class Scene:
    def __init__(self):
        self.camera = Camera()
        self.camera.rotation = [-0.3, 0.5, 0]
        self.animator = Animator()

        self.background: Background = Background((0.2, 0.2, 0.2), (0.5, 0.5, 0.5))
        self.cube = Cube((7, 5, 3))

    def render(self, width: int, height: int, delta_time: float) -> None:
        glDisable(GL_DEPTH_TEST)
        self.background.draw()

        glEnable(GL_DEPTH_TEST)
        glClear(GL_DEPTH_BUFFER_BIT)
        self.animator.run(delta_time)

        camera_transform = self.camera.position_transform().to_ctypes()
        camera_perspective = self.camera.perspective_transform(width, height).to_ctypes()
        self.cube.draw(camera_transform, camera_perspective)

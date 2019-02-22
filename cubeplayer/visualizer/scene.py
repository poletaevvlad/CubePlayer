from OpenGL.GL import *

from ctypes import *
from pathlib import Path

from .shaders import Program
from .vbo import create_background, load_obj
from .camera import Camera


class Scene:
    def __init__(self):
        self.camera = Camera()
        self.shader = Program("background")
        self.object_shader = Program("object")
        self.background = create_background()
        self.object = load_obj(Path(__file__).parents[2] / "models" / "monkey.obj")

    def render(self, width: int, height: int) -> None:
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.object_shader.use()
        transform = self.camera.transform(width, height).to_ctypes()
        glUniformMatrix4fv(self.object_shader.uniforms["cameraTransform"], 1, GL_FALSE, transform)

        self.object.bind()
        glDrawElements(GL_TRIANGLES, self.object.elements_count, GL_UNSIGNED_SHORT, c_void_p(0))

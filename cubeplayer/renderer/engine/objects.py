from abc import ABC
from ctypes import c_float
from typing import Tuple

from OpenGL.GL import *

from .shaders import Program
from .vbo import VAO, create_quad

ColorType = Tuple[float, float, float]


class Object3d(ABC):
    def __init__(self, vao: VAO, material: Program):
        self.vao: VAO = vao
        self.material: Program = material


class Background(Object3d):
    # noinspection PyTypeChecker, PyCallingNonCallable
    def __init__(self, gradient_to: ColorType, gradient_from: ColorType):
        vao = create_quad()
        shader = Program("background")
        super(Background, self).__init__(vao, shader)

        color_type = c_float * 3
        shader.use()
        glUniform3fv(self.material.uniforms["colorFrom"], 1, color_type(*gradient_to))
        glUniform3fv(self.material.uniforms["colorTo"], 1, color_type(*gradient_from))

    def draw(self) -> None:
        self.material.use()
        self.vao.draw()

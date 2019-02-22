from .shaders import Program
from .vbo import VAO, create_background

from OpenGL.GL import *
from abc import ABC, abstractmethod
from typing import Tuple
from ctypes import c_float, c_void_p

ColorType = Tuple[float, float, float]


class Object3d(ABC):
    def __init__(self, vao: VAO, material: Program):
        self.vao: VAO = vao
        self.material: Program = material

    @abstractmethod
    def draw(self) -> None:
        pass

    def destroy(self) -> None:
        self.vao.destroy()
        self.material.destroy()


class Background(Object3d):
    # noinspection PyTypeChecker, PyCallingNonCallable
    def __init__(self, gradient_to: ColorType, gradient_from: ColorType):
        vao = create_background()
        shader = Program("background")
        super(Background, self).__init__(vao, shader)

        color_type = c_float * 3
        self.gradient_to: ColorType = color_type(*gradient_to)
        self.gradient_from: ColorType = color_type(*gradient_from)

    def draw(self) -> None:
        self.material.use()
        glUniform3fv(self.material.uniforms["colorFrom"], 1, self.gradient_from)
        glUniform3fv(self.material.uniforms["colorTo"], 1, self.gradient_to)

        self.vao.bind()
        glDrawElements(GL_TRIANGLES, self.vao.elements_count, GL_UNSIGNED_SHORT, c_void_p(0))

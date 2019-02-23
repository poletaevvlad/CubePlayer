from .shaders import Program
from .vbo import VAO, create_background, load_obj

from OpenGL.GL import *
from abc import ABC
from typing import Tuple
from ctypes import c_float, c_void_p, Array
from pathlib import Path

ColorType = Tuple[float, float, float]
nullptr = c_void_p(0)


class Object3d(ABC):
    def __init__(self, vao: VAO, material: Program):
        self.vao: VAO = vao
        self.material: Program = material


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
        glDrawElements(GL_TRIANGLES, self.vao.elements_count, GL_UNSIGNED_SHORT, nullptr)


class CubeComponent(Object3d):
    _shader: Program = None

    def __init__(self):
        shader = CubeComponent._shader
        if shader is None:
            shader = Program("object")
            CubeComponent._shader = shader

        vao = load_obj(Path(__file__).parents[2] / "models" / "monkey.obj")
        super(CubeComponent, self).__init__(vao, shader)

    def draw(self, camera_transform: Array, camera_projection: Array) -> None:
        self.material.use()
        glUniformMatrix4fv(self.material.uniforms["cameraTransform"], 1, GL_TRUE, camera_transform)
        glUniformMatrix4fv(self.material.uniforms["cameraProjection"], 1, GL_TRUE, camera_projection)

        self.vao.bind()
        glDrawElements(GL_TRIANGLES, self.vao.elements_count, GL_UNSIGNED_SHORT, nullptr)

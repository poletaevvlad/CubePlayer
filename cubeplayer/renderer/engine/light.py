from typing import  Tuple, Iterable
from math import sqrt

from OpenGL.GL import *

from .shaders import Program

Vec3 = Tuple[float, float, float]


def normalize(vec: Vec3) -> Vec3:
    x, y, z = vec
    magnitude = sqrt(x * x + y * y + z * z)
    return x / magnitude, y / magnitude, z / magnitude


class DirectionalLight:
    def __init__(self, color: Vec3, direction: Vec3):
        self.color: Vec3 = color
        self.direction: Vec3 = normalize(direction)

    def push_uniform(self, shader: Program, var: str) -> None:
        glUniform3f(shader.uniforms[var + ".color"], *self.color)
        glUniform3f(shader.uniforms[var + ".direction"], *self.direction)

    @staticmethod
    def push_uniform_array(shader: Program, array: str, lights: Iterable["DirectionalLight"]) -> None:
        for i, light in enumerate(lights):
            light.push_uniform(shader, f"{array}[{i}]")

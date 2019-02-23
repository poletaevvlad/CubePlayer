from OpenGL.GL import *
from typing import Dict

from pathlib import Path

SHADERS_DIR = Path(__file__).parents[2] / "shaders"


class Shader:
    def __init__(self, filename: str, kind: GLuint):
        file = str(SHADERS_DIR / filename)
        with open(file) as f:
            contents = f.read()

        self.shader_id = glCreateShader(kind)
        glShaderSource(self.shader_id, contents)
        glCompileShader(self.shader_id)

        if glGetShaderiv(self.shader_id, GL_COMPILE_STATUS) == GL_FALSE:
            log = glGetShaderInfoLog(self.shader_id)
            self.destroy()
            raise RuntimeError(log)

    def destroy(self):
        glDeleteShader(self.shader_id)


class Program:
    def __init__(self, filename: str):
        self.vertex = Shader(filename + ".vert", GL_VERTEX_SHADER)
        try:
            self.fragment = Shader(filename + ".frag", GL_FRAGMENT_SHADER)
        except RuntimeError:
            self.vertex.destroy()
            raise

        self.program_id = glCreateProgram()
        glAttachShader(self.program_id, self.vertex.shader_id)
        glAttachShader(self.program_id, self.fragment.shader_id)
        glLinkProgram(self.program_id)

        if glGetProgramiv(self.program_id, GL_LINK_STATUS) != GL_TRUE:
            log = glGetProgramInfoLog(self.program_id)
            self.destroy()
            raise RuntimeError(log)
        self.uniforms = Uniforms(self)

    def use(self):
        glUseProgram(self.program_id)

    def destroy(self):
        glDetachShader(self.program_id, self.vertex.shader_id)
        self.vertex.destroy()
        glDetachShader(self.program_id, self.fragment.shader_id)
        self.fragment.destroy()
        glDeleteProgram(self.program_id)


class Uniforms:
    def __init__(self, program: Program):
        self.uniforms: Dict[str, GLint] = dict()
        self.program: Program = program

    def __getitem__(self, item: str) -> GLint:
        if item in self.uniforms:
            return self.uniforms[item]
        location = glGetUniformLocation(self.program.program_id, item)
        if location == -1:
            raise ValueError(f"Unknown uniform: {item}")
        self.uniforms[item] = location
        return location

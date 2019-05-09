from OpenGL.GL import *

from .texture import Texture
from .vbo import VAO, create_quad
from .shaders import Program


class Sprite:
    quad: VAO = None
    shader: Program = None

    def __init__(self, width: int, height: int, texture: Texture):
        self.width = width
        self.height = height
        self.texture = texture

        if Sprite.quad is None:
            Sprite.quad = create_quad()
        if Sprite.shader is None:
            Sprite.shader = Program("sprite")

    def draw(self, screen_width: int, screen_height: int, x: int, y: int):
        Sprite.shader.use()
        glUniform2f(Sprite.shader.uniforms["size"], self.width, self.height)
        glUniform2f(Sprite.shader.uniforms["screen_size"], screen_width,
                    screen_height)
        glUniform2f(Sprite.shader.uniforms["location"], x, y)
        self.texture.activate(0)
        glUniform1i(Sprite.shader.uniforms["tex"], 0)

        Sprite.quad.draw()

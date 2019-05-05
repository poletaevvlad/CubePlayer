from attr import dataclass
from freetype import *
from pathlib import Path
from typing import Dict
from OpenGL.GL import *

from .objects import nullptr
from .vbo import create_quad
from .shaders import Program


@dataclass
class Character:
    bitmap_width: int
    bitmap_rows: int
    texture_id: int
    texture_size: int
    x_offset: float
    y_offset: float
    advance: float


def _to_power_2(num):
    x = 1
    while x < num:
        x <<= 1
    return x


class FontFace:
    def __init__(self, font_file: Path, size: float):
        # noinspection PyTypeChecker
        self.face = Face(str(font_file))
        self.face.set_char_size(int(64 * size))
        self.characters: Dict[str, Character] = dict()
        self.vao = create_quad()

        self.shader = Program("text")
        self.shader.use()
        glUniform3f(self.shader.uniforms["color"], 1.0, 1.0, 1.0)
        glUniform1i(self.shader.uniforms["char_bitmap"], 0)

    def get_character(self, char: str) -> Character:
        if char in self.characters:
            return self.characters[char]

        # noinspection PyUnresolvedReferences
        self.face.load_char(char, FT_LOAD_RENDER)
        bitmap: Bitmap = self.face.glyph.bitmap

        tex_size = _to_power_2(max(bitmap.width, bitmap.rows))
        data = bytearray(tex_size * tex_size)
        for i in range(bitmap.rows):
            for j in range(bitmap.width):
                data[i * tex_size + j] = bitmap.buffer[i * bitmap.width + j]

        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, tex_size, tex_size, 0,
                     GL_RED, GL_UNSIGNED_BYTE, data)

        character = Character(bitmap_width=bitmap.width, texture_size=tex_size,
                              bitmap_rows=bitmap.rows, texture_id=tex_id,
                              advance=self.face.glyph.advance.x / 64,
                              x_offset=self.face.glyph.bitmap_left,
                              y_offset=self.face.glyph.bitmap_top - bitmap.rows)
        self.characters[char] = character
        return character

    def draw(self, screen_width: int, screen_height: int, x: int, y: int,
             text: str):

        self.shader.use()
        glUniform2f(self.shader.uniforms["screen_size"], screen_width, screen_height)

        prev_c = None
        for c in text:
            if prev_c is not None:
                x += self.face.get_kerning(prev_c, c).x
            prev_c = c

            char = self.get_character(c)
            glUniform2f(self.shader.uniforms["uv_scale"],
                        char.bitmap_width / char.texture_size,
                        char.bitmap_rows / char.texture_size)

            glUniform2f(self.shader.uniforms["location"], x + char.x_offset, y - char.y_offset)
            glUniform2f(self.shader.uniforms["size"], char.bitmap_width, char.bitmap_rows)

            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, char.texture_id)

            self.vao.bind()
            glDrawElements(GL_TRIANGLES, self.vao.elements_count, GL_UNSIGNED_SHORT,
                           nullptr)

            x += char.advance

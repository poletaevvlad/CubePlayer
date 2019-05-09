from OpenGL.GL import *
from PIL import Image

from pathlib import Path


class Texture:
    def __init__(self, path: Path, format: GLint = GL_RGB, flip: bool = False):
        self.id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.id)

        img: Image = Image.open(str(path))
        if format == GL_RGB:
            img = img.convert("RGB")
        elif format == GL_RGBA:
            img = img.convert("RGBA")
        if flip:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
        glTexImage2D(GL_TEXTURE_2D, 0, format, *img.size, 0, format, GL_UNSIGNED_BYTE, img.tobytes())
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    @staticmethod
    def load(filename: str, format: GLint = GL_RGB, flip: bool = False):
        path = Path(__file__).parents[3] / "textures" / (filename + ".png")
        return Texture(path, format, flip)

    def activate(self, index: int) -> None:
        glActiveTexture(GL_TEXTURE0 + index)
        glBindTexture(GL_TEXTURE_2D, self.id)

    def destroy(self) -> None:
        glDeleteTextures(self.id)

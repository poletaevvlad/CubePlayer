from OpenGL.GL import *
from pathlib import Path
from typing import Sequence
from .engine.text import FontFace
from .engine.texture import Texture
from .engine.sprite import Sprite


class FormulaUI:
    def __init__(self, items: Sequence[str]):
        self.items = items
        self.position: float = 0
        self.item_width: int = 45

        path = Path(__file__).parents[2] / "fonts" / "PT_Sans-Regular.ttf"
        self.font = FontFace(path, 16)
        self.indicator = Sprite(16, 16, Texture.load("ui_indicator", GL_RGBA))
        self.separator = Sprite(16, 16, Texture.load("ui_separator", GL_RGBA,
                                                     filter=GL_NEAREST))

    def render(self, width: int, height: int):
        leftmost = round(width / 2- self.position * self.item_width)
        if leftmost > 0:
            index = 0
        else:
            index = -leftmost // self.item_width

        position = leftmost + self.item_width * index
        while position < width and index < len(self.items):
            self.separator.draw(width, height,
                                position - self.separator.width // 2,
                                height - self.separator.height - 10)

            self.font.draw(width, height, position + self.item_width // 2,
                           height - 13, self.items[index], align=0.5)

            index += 1
            position += self.item_width

        self.separator.draw(width, height,
                            position - self.separator.width // 2,
                            height - self.separator.height - 10)
        self.indicator.draw(width, height, (width - self.indicator.width) // 2,
                            height - self.indicator.height)

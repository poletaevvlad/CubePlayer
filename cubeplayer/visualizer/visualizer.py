from gi.repository import Gtk
from gi.repository import Gdk
from OpenGL.GL import *

from ctypes import *
from pathlib import Path

from .shaders import Program
from .vbo import create_background, load_obj
from .camera import Camera


# noinspection PyMethodMayBeStatic
class CubeVisualizer(Gtk.GLArea):
    def __init__(self):
        Gtk.GLArea.__init__(self)
        self.connect("realize", self.on_realize)
        self.connect("render", self.on_render)
        self.set_has_depth_buffer(True)

        self.shader = None
        self.background = None
        self.object = None
        self.object_shader: Program = None
        self.camera = Camera()

    def on_realize(self, _area: Gtk.GLArea) -> None:
        ctx = self.get_context()
        ctx.make_current()

        self.shader = Program("background")
        self.object_shader = Program("object")
        self.background = create_background()
        self.object = load_obj(Path(__file__).parents[2] / "models" / "monkey.obj")

    def on_render(self, _area: Gtk.GLArea, ctx: Gdk.GLContext):
        ctx.make_current()

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.object_shader.use()

        transform = self.camera.transform(self.get_allocation().width, self.get_allocation().height).to_ctypes()
        glUniformMatrix4fv(self.object_shader.uniforms["cameraTransform"], 1, GL_FALSE, transform)
        self.object.bind()
        glDrawElements(GL_TRIANGLES, self.object.elements_count, GL_UNSIGNED_SHORT, c_void_p(0))

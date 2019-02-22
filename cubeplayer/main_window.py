from gettext import gettext

from gi.repository import Gtk
from gi.repository import Gdk
from visualizer import Scene


_ = gettext


class CubeVisualizer(Gtk.GLArea):
    def __init__(self):
        Gtk.GLArea.__init__(self)
        self.set_has_depth_buffer(True)
        self.connect("realize", self.on_realize)
        self.connect("render", self.on_render)
        self.scene: Scene = None

    def on_realize(self, _area: Gtk.GLArea) -> None:
        ctx = self.get_context()
        ctx.make_current()
        self.scene = Scene()

    def on_render(self, _area: Gtk.GLArea, ctx: Gdk.GLContext) -> None:
        ctx.make_current()

        allocation = self.get_allocation()
        self.scene.render(allocation.width, allocation.height)


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, application):
        super().__init__(application=application)
        self.set_size_request(800, 600)

        view = CubeVisualizer()
        self.add(view)
        view.show()

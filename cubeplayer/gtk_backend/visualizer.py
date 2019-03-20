from typing import Callable

from gi.repository import Gdk
from gi.repository import Gtk

from ..renderer.scene import Scene


class CubeVisualizer(Gtk.GLArea):
    def __init__(self, realize_callback: Callable[[Scene], None]):
        Gtk.GLArea.__init__(self)
        self.set_has_depth_buffer(True)
        self.connect("realize", self.on_realize)
        self.connect("render", self.on_render)
        self.realize_callback = realize_callback

        self.set_events(Gdk.EventMask.BUTTON1_MOTION_MASK | Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect("motion_notify_event", self.on_motion)
        self.connect("button_press_event", self.on_button_press)

        self.scene: Scene = None

        self.drag_x: float = float("nan")
        self.drag_y: float = float("nan")

    def on_realize(self, _area: Gtk.GLArea) -> None:
        ctx = self.get_context()
        ctx.make_current()
        self.scene = Scene()
        self.realize_callback(self.scene)
        self.realize_callback = None

    def on_render(self, _area: Gtk.GLArea, ctx: Gdk.GLContext) -> bool:
        ctx.make_current()
        allocation = self.get_allocation()
        self.scene.render(allocation.width, allocation.height)
        return False

    def on_motion(self, _widget: Gtk.Widget, event: Gdk.EventMotion):
        delta_x = event.x - self.drag_x
        delta_y = event.y - self.drag_y
        self.scene.rotate(delta_x, delta_y)
        self.drag_x = event.x
        self.drag_y = event.y

    def on_button_press(self, _widget: Gtk.Widget, event: Gdk.EventButton):
        self.drag_x = event.x
        self.drag_y = event.y

from time import time
from typing import List, Optional

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib

from ..renderer.scene import Scene
from libcube.actions import Action


class CubeVisualizer(Gtk.GLArea):
    def __init__(self):
        Gtk.GLArea.__init__(self)
        self.set_has_depth_buffer(True)
        self.connect("realize", self.on_realize)
        self.connect("render", self.on_render)

        # self.set_events(Gdk.EventMask.BUTTON1_MOTION_MASK | Gdk.EventMask.BUTTON_PRESS_MASK)
        # self.connect("motion_notify_event", self.on_motion)
        # self.connect("button_press_event", self.on_button_press)

        # self.add_tick_callback(self.on_tick, None)
        self.scene: Scene = None
        self.last_frame_time = None
        self.init_formula: Optional[List[Action]] = None

        self.drag_x: float = float("nan")
        self.drag_y: float = float("nan")

    def on_realize(self, _area: Gtk.GLArea) -> None:
        ctx = self.get_context()
        ctx.make_current()
        self.scene = Scene()
        if self.init_formula is not None:
            self.scene.run_formula(self.init_formula)
            self.init_formula = None

    def on_render(self, _area: Gtk.GLArea, ctx: Gdk.GLContext) -> bool:
        ctx.make_current()

        current_time = time()
        delta_time = 0 if self.last_frame_time is None else current_time - self.last_frame_time
        self.last_frame_time = current_time

        allocation = self.get_allocation()
        self.scene.render(allocation.width, allocation.height, delta_time)
        return False

    def on_tick(self, _area: Gtk.GLArea, _frame_clock: Gdk.FrameClock, _user_data: None) -> bool:
        self.queue_draw()
        return GLib.SOURCE_CONTINUE

    def set_formula(self, formula: List[Action]) -> None:
        if self.scene is None:
            self.init_formula = formula
        else:
            self.scene.run_formula(formula)

    def on_motion(self, _widget: Gtk.Widget, event: Gdk.EventMotion):
        delta_x = event.x - self.drag_x
        delta_y = event.y - self.drag_y
        self.scene.rotate(delta_x, delta_y)
        self.drag_x = event.x
        self.drag_y = event.y

    def on_button_press(self, _widget: Gtk.Widget, event: Gdk.EventButton):
        self.drag_x = event.x
        self.drag_y = event.y

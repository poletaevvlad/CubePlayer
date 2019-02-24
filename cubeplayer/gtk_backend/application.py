import gi
gi.require_version("Gtk", "3.0")
gi.require_version("GtkSource", "3.0")
from gi.repository import Gtk

from .window import MainWindow


class Application(Gtk.Application):
    APP_ID = "io.github.poletaevvlad.cubeplayer"

    def __init__(self):
        super().__init__(application_id=Application.APP_ID)

    def do_activate(self):
        window = MainWindow(application=self)
        window.present()

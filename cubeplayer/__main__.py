from libcube.actions import Action
from cubeplayer.parsing import CubeFormulaParamType

from typing import List
import signal

import click


def run_gtk(formula: List[Action]):
    import gi
    gi.require_version("Gtk", "3.0")
    gi.require_version("GtkSource", "3.0")
    from gi.repository import Gtk
    from cubeplayer.gtk_backend import MainWindow

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    window = MainWindow(formula)
    window.show()
    window.connect("destroy", Gtk.main_quit)
    Gtk.main()


@click.command()
@click.option("-b", "backend", type=click.Choice(["gtk"]), default="gtk")
@click.argument("formula", type=CubeFormulaParamType())
def main(formula: List[Action], backend: str) -> None:
    run_gtk(formula)


if __name__ == "__main__":
    # noinspection PyArgumentList
    main()

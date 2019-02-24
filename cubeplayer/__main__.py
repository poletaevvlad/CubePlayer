import signal
import sys
from cubeplayer.gtk_backend import Application


signal.signal(signal.SIGINT, signal.SIG_DFL)
app = Application()
app.run(sys.argv)

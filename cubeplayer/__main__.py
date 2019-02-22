import signal
from main import Application
import sys


signal.signal(signal.SIGINT, signal.SIG_DFL)
app = Application()
app.run(sys.argv)

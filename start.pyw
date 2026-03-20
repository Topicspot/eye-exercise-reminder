# start.pyw — Silent launcher (no console window)
# Double-click this file to run the app without a terminal.
# On Windows, .pyw files are executed by pythonw.exe — no console opens.

import runpy, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
runpy.run_module("eye_reminder", run_name="__main__", alter_sys=True)

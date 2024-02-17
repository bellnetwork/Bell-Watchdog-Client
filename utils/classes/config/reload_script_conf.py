import os, sys
from watchdog.events import FileSystemEventHandler

class ReloadScriptEventHandler(FileSystemEventHandler):
    """Handles filesystem events to reload the script."""
    def __init__(self, script_name):
        self.script_name = script_name

    def on_modified(self, event):
        if not event.is_directory and event.src_path == self.script_name:
            print(f"Detected a change in {event.src_path}. Reloading the script.")
            os.execl(sys.executable, sys.executable, *sys.argv)
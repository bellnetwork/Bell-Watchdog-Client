# if_name_conf.py

import asyncio, sys, os
from watchdog.observers import Observer
from utils.sys.websocket.connect import main
from utils.classes.config.reload_script_conf import ReloadScriptEventHandler

def conf_if_name(sio):
    # Start the observer thread that monitors file changes
    path_to_watch = "/path/to/your/project"  # Adjust the path to your project directory
    event_handler = ReloadScriptEventHandler(__file__)
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=False)
    observer.start()

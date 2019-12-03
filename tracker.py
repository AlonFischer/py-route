#!/usr/bin/env python
# coding=utf-8

from watchdog.observers import Observer
from watchdog.events import *
import time
import os 

CONFIG_FILE = "./config.json"
TASK = "sudo python main.py"

class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_modified(self, event):
        if event.src_path == CONFIG_FILE:
            print("[+] Updating configs")
            try:
                os.system(TASK)
            except:
                print("error while executing cmd"+ TASK )

if __name__ == "__main__":
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler,".",True)
    observer.start()
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

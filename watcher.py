#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Watcher looks for file creations and changes
"""

import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

#Define varibles 
patterns = ["*.pdf", "*.txt"]              #file patterns we want to handle
ignore_patterns = ""        #file patterns we want to exclude, here no other files
ignore_directories = False  # directories which shall not be watched
case_sensitive = True       # Important: windows' file system is case insensitive!

path = "./.."              #define start path to be watched
go_recursively = True   # define whether subdirectories will be watched


def on_created(event):
    print(f"File created: {event.src_path}")

def on_deleted(event):
    print(f"File deleted: {event.src_path}")

def on_modified(event):
    print(f"File modified: {event.src_path}")

def on_moved(event):
    print(f"File moved: from {event.src_path} to {event.dest_path}")

if __name__ == "__main__":

    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)


    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved


    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)   # sleep for x seconds
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()





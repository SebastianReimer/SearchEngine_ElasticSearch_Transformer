#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Watcher looks for file creations and changes
"""
import logging
from pathlib import Path
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from tika import parser
from haystack.database.elasticsearch import ElasticsearchDocumentStore
from indexing.io import write_texts_to_db


# create logger 
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


#Define varibles 
patterns = ["*.pdf", "*.txt"]              #file patterns we want to handle
ignore_patterns = ""        #file patterns we want to exclude, here no other files
ignore_directories = False  # directories which shall not be watched
case_sensitive = True       # Important: windows' file system is case insensitive!

path = Path("./data")              #define start path to be watched
logger.info(f"path(s) to be oberserved:\n{path.absolute()} ")
go_recursively = True   # define whether subdirectories will be watched

sleep_time = 1 # interval ([seconds]) in which paths will be watched

document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")

def on_created(event):
    """
    If text file is created, content is parsed and ingested into DB

    :param event: 
    :return: None
    """
    parsed_data = parser.from_file(event.src_path, 'http://localhost:9998/tika')
    parsed_text = str(parsed_data['content'])



    write_texts_to_db(text=parsed_text,
                    path_name=event.src_path, 
                    document_store=document_store,
                    clean_func=None, 
                    only_empty_db=False, 
                    split_paragraphs=False)
    logger.info(f"File created: {event.src_path}")
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
    my_observer.schedule(my_event_handler, str(path.absolute()), recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(sleep_time)   # sleep for x seconds
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()





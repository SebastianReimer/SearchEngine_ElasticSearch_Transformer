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
#from haystack.database.elasticsearch import ElasticsearchDocumentStore
from DocumentStore import ES_DocumentStore
import hashlib
from indexing.io import write_texts_to_db, update_text, update_text_docid, _create_hash, get_all_files


# create logger 
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


#Define varibles 
patterns = ["*.pdf", "*.txt", "*.docx"]              #file patterns we want to handle
ignore_patterns = ""        #file patterns we want to exclude, here no other files
ignore_directories = False  # directories which shall not be watched
case_sensitive = True       # Important: windows' file system is case insensitive!

path = Path("./data")              #define start path to be watched
logger.info(f"path(s) to be oberserved:\n{path.absolute()} ")
go_recursively = True   # define whether subdirectories will be watched

sleep_time = 1 # interval ([seconds]) in which paths will be watched

# = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")
es_docstore = ES_DocumentStore(host = 'localhost',
                username= "",
                password="",
                scheme="http",
                index ='document',
                ca_certs=False,
                verify_certs=True)

def on_created(event):
    #delete because it is not needed hence  on_modified 
    pass
def on_deleted(event):
    """
    Deletes the entry for a the deleted file in the DB

    :param event: 
    :return: None
    """
    path_name = event.src_path
    doc_id = _create_hash(path_name)

    query = { "bool": {"must":{"term" :{"doc_id":f"{doc_id}"}}}}
    es_docstore.client.delete_by_query(index=es_docstore.index, body={"query":query}, refresh=True)
    logger.info(f"File deleted from DB: {event.src_path}")

def on_modified(event):
    """
    If a text file is created, the content is parsed and ingested into DB.
    If a text file is modified, the content is parsed an updated  in the DB

    :param event: 
    :return: None
    """
    path_name = event.src_path
    parsed_data = parser.from_file(path_name, 'http://localhost:9998/tika')
    parsed_text = str(parsed_data['content'])

    doc_id = _create_hash(path_name)
    
    #check if file already exists in db
    query = { "bool": {"must":{"term" :{"doc_id":f"{doc_id}"}}}}
    res = es_docstore.client.search(index=es_docstore.index, body={"query":query})

    if (len(res['hits']['hits']) == 0):
        # load data into DB
        write_texts_to_db(text=parsed_text,
                    path_name=event.src_path, 
                    document_store=es_docstore,
                    clean_func=None, 
                    only_empty_db=False, 
                    split_paragraphs=False)
        logger.info(f"File created in DB: {event.src_path}")
        
    else:
        # Update data in DB
        update_text(document_store=es_docstore,
                    index=es_docstore.index,
                    path_name=event.src_path,
                    doc_id=doc_id,
                    parsed_text=parsed_text)
        logger.info(f"File modified in DB: {event.src_path}")


def on_moved(event):
    """
    If a file is moved in the file system, the path (and the corresponding doc_id)
    is updated in the DB

    :param event: 
    :return: None
    """
    source_path_name = event.src_path
    source_doc_id = _create_hash(source_path_name)

    dest_path_name = event.dest_path
    dest_doc_id = _create_hash(dest_path_name)

    update_text_docid(document_store=es_docstore,
                        index=es_docstore.index,
                        source_doc_id=source_doc_id,
                        dest_doc_id=dest_doc_id,
                        dest_path_name=dest_path_name)

    logger.info(f"File moved: from {event.src_path} to {event.dest_path}")



if __name__ == "__main__":

    #first: scan through file system and check if there are any changes
    all_files = get_all_files(patterns=patterns, path=path)
    print(all_files)

    for file_path in all_files:
        if (es_docstore.file_exists_in_db(file_path=file_path)): # if file is already in DB
            #file exists
            if (es_docstore.check_modtime_changed(file_path=file_path)): # check if files was changed
                #file was changed
                parsed_data = parser.from_file(file_path, 'http://localhost:9998/tika')
                parsed_text = str(parsed_data['content'])
                doc_id = _create_hash(file_path)
                update_text(document_store=es_docstore,
                    index=es_docstore.index,
                    path_name=file_path,
                    doc_id=doc_id,
                    parsed_text=parsed_text)
                logger.info(f"File modified in DB: {file_path}")
        else:
            #file does not exist   
            parsed_data = parser.from_file(file_path, 'http://localhost:9998/tika')
            parsed_text = str(parsed_data['content'])
            write_texts_to_db(text=parsed_text,
                    path_name=file_path, 
                    document_store=es_docstore,
                    clean_func=None, 
                    only_empty_db=False, 
                    split_paragraphs=False)
            logger.info(f"File created in DB: {file_path}")  

    #second: check if there any dangling entries in the db which means that there are no
    # corresponding files in the filesystem 
    inDB_notFile = es_docstore.docs_exists_as_files(all_files) #these entries need to be deleted from the db
    if (inDB_notFile):
        es_docstore.delete_documents(inDB_notFile)
    '''
    #third: start watcher which keeps track of file changes
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

    '''



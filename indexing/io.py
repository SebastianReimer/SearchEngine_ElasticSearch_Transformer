#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import logging
import hashlib

logger = logging.getLogger(__name__)

def write_texts_to_db(text, path_name, document_store, clean_func=None, only_empty_db=False, split_paragraphs=False):
    """
    Writes text to the connected database.

    :param text: text which should be ingested to the database
    :param path_name: path for the file whose text should be uploaded to the database
    :param clean_func: a custom cleaning function that gets applied to each doc (input: str, output:str)
    :param only_empty_db: If true, docs will only be written if db is completely empty.
                              Useful to avoid indexing the same initial docs again and again.
    :return: None
    """
    #get absolute path as string
    path = Path(path_name)
    abs_path = str(path.absolute())
    
    if only_empty_db:
        n_docs = document_store.get_document_count()
        if n_docs > 0:
            logger.info(f"Skip writing documents since DB already contains {n_docs} docs ...  "
                        "(Disable `only_empty_db`, if you want to add docs anyway.)")
            return None

    docs_to_index = []

    # hash the path for an document identifier
    doc_id = hashlib.md5(abs_path.encode()) 

    if split_paragraphs:
        for para in text.split("\n\n"):
            if not para.strip():  # skip empty paragraphs
                continue
            docs_to_index.append(
                    {   "doc_id": doc_id.hexdigest(), 
                        "name": abs_path,
                        "text": para
                    }
                )
                    
    else:
        docs_to_index.append(
                    {   "doc_id": doc_id.hexdigest(), 
                        "name": abs_path,
                        "text": text
                    }
                )

    document_store.write_documents(docs_to_index)
    logger.info(f"Wrote text docs to DB")

def update_text(document_store, index, doc_id, parsed_text):
        """
        Updates the text field of document in the DB

        :param document_store: An ElasticSearchDocumentStore
        :param index: Index, where the document is located to be updated
        :param doc_id: Document identifier as a hash
        :param parsed_text: Text which should be updated in the corressponding text field
        :return: None
        """
        script =  {"source" : f"ctx._source['text'] = '{parsed_text}'"}
        query = { "bool": {"must":{"term" :{"doc_id":f"{doc_id}"}}}}
        document_store.client.update_by_query(index=index, body={"script": script, "query": query})
        logger.info(f"Updated text from changed file.")

def update_text_docid(document_store, index, source_doc_id, dest_doc_id, dest_path_name):
        """
        Updates the name (path) field and the doc_id field of document in the DB
        if a file ist moved on the file system.

        :param document_store: An ElasticSearchDocumentStore
        :param index: Index, where the document is located to be updated
        :param source_doc_id: Document identifier as a hash for the source file
        :param dest_id: Document identifier as a hash for the destination file
        :param dest_path_name: Path name of the destination file
        :return: None
        """
        script =  {"source" : f"ctx._source['name'] = '{dest_path_name}'; ctx._source['doc_id'] = '{dest_doc_id}'" }
        logger.debug(f"Source_doc_id: {source_doc_id}")
        logger.debug(f"dest_doc_id: {dest_doc_id}")
        query = { "bool": {"must":{"term" :{"doc_id":f"{source_doc_id}"}}}}
        document_store.client.update_by_query(index=index, body={"script": script, "query": query})
        logger.info(f"Updated text from changed file.")
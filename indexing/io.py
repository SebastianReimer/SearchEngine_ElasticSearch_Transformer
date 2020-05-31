#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import logging

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
    path = Path(path_name)

    
    if only_empty_db:
        n_docs = document_store.get_document_count()
        if n_docs > 0:
            logger.info(f"Skip writing documents since DB already contains {n_docs} docs ...  "
                        "(Disable `only_empty_db`, if you want to add docs anyway.)")
            return None

    docs_to_index = []

    if split_paragraphs:
        for para in text.split("\n\n"):
            if not para.strip():  # skip empty paragraphs
                continue
            docs_to_index.append(
                    {
                        "name": path.name,
                        "text": para
                    }
                )
                    
    else:
        docs_to_index.append(
                    {
                        "name": path.name,
                        "text": text
                    }
                )

    document_store.write_documents(docs_to_index)
    logger.info(f"Wrote text docs to DB")
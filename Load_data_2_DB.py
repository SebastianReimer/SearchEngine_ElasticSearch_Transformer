#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Load preprocessed text files into ES
"""

import logging
import subprocess
import time

from haystack import Finder
from haystack.database.elasticsearch import ElasticsearchDocumentStore
from haystack.indexing.cleaning import clean_wiki_text
from haystack.indexing.io import write_documents_to_db, fetch_archive_from_http
from haystack.reader.farm import FARMReader
from haystack.reader.transformers import TransformersReader
from haystack.utils import print_answers
from haystack.retriever.elasticsearch import ElasticsearchRetriever



#load data into ES

doc_dir = "/home/sebastian/SideProject/QA/wikiextractor/preprocessed/folder_1"
document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")
write_documents_to_db(document_store=document_store,
                      document_dir=doc_dir, 
                      #clean_func=clean_wiki_text, 
                      only_empty_db=False, 
                      split_paragraphs=True)

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import logging
from indexing.io import _create_hash, _get_modtime

logger = logging.getLogger(__name__)

class ES_DocumentStore:
    def __init__(self, host, username, password, index, scheme, ca_certs, verify_certs):
        self.host = host
        self.username = username
        self.password = password
        self.index = index
        self.scheme = scheme
        self.ca_certs = ca_certs
        self.verify_certs = verify_certs
        self.client = Elasticsearch(hosts=[{"host": host}], http_auth=(username, password),
                                    scheme=scheme, ca_certs=ca_certs, verify_certs=verify_certs)

    def write_documents(self, documents):
        for doc in documents:
            doc["_op_type"] = "create"
            doc["_index"] = self.index

        bulk(self.client, documents, request_timeout=30)
    
    def delete_documents(self, documents):
        """
        Deletes documents in the db 

        :param documents: list containing the files to be deleted
        :return: 
        """

        doc_ids = [_create_hash(file) for file in documents]
        
        for i, doc_id in enumerate(doc_ids):
            query = { "bool": {"must":{"term" :{"doc_id":f"{doc_id}"}}}}
            self.client.delete_by_query(index=self.index, body={"query":query}, refresh=True)
            logger.info(f"File deleted from DB: {documents[i]}")

    def get_document_count(self):
        result = self.client.count()
        count = result["count"]
        return count

    def check_index_empty(self):
        """
        Writes text to the connected database.

        :param document_store: Instance of ES_DocumentStore
        :return: True or False whether index is empty or not
        """
        res = self.client.search(index=self.index) 
        if (res['hits']['total']['value'] == 0):
            return True
        else:
            return False

    def file_exists_in_db(self, file_path):
        """
        Checks whether a file already exists in the db

        :param file_path: absolute file path
        :param path: root path as starting point
        :return: True or False whether file exists in db or not
        """
        doc_id = _create_hash(file_path)

        query = { "bool": {"must":{"term" :{"doc_id":f"{doc_id}"}}}}
        res = self.client.search(index=self.index, body={"query":query})
        if (res['hits']['total']['value'] == 1):
            return True
        else:
            return False

    def docs_exists_as_files(self, all_files):
        """
        Checks whether for documents in the db there are the corresponding
        files on the filesystem 

        :param all_files: A list containing all absolute paths for files
        :return inDB_notFile: A list containing files which are in the database, but do not exists as files anymore
        """
        res = self.client.search(index=self.index, _source=['name'])
        files_db = [hit['_source']['name'] for hit in res['hits']['hits']]

        inDB_notFile = []# in Database but not in file system
        for doc in files_db:
            if (doc not in all_files):
                inDB_notFile.append(doc)
        return inDB_notFile

    def check_modtime_changed(self,file_path):
        """
        Compares the modification time a file on the file system with modification time (ts) in the db 

        :param file_path: absolute file path
        :return: True or False whether a file was changed or not 
        """
        doc_id = _create_hash(file_path)
        #get modification time from file
        ts_file, _ = _get_modtime(file_path)

        #get modification from db
        query = { "bool": {"must":{"term" :{"doc_id":f"{doc_id}"}}}}
        res = self.client.search(index=self.index, body={"query":query}, _source=['ts'])
        ts_db = int()
        try:
            if (res['hits']['total']['value'] == 1):
                ts_db = res['hits']['hits'][0]['_source']['ts']
                
        except:
            print("Exception: Returned to many/or less results")

        if (ts_file != ts_db):
            return True
        else: 
            return False
    

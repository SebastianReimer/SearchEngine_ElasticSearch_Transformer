from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import logging

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

    def get_document_count(self):
        result = self.client.count()
        count = result["count"]
        return count
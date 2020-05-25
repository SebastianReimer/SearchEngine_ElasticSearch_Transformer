'''
import requests,json

headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
}


payload = {
                "query": {
                    "query_string": {
                        "analyze_wildcard": True,
                        "query": "Sansa", # str(search_term)
                        "fields": ["name", "text", "_score"]
                    }
                },
                "size": 50,
                "sort": [

                ]
            }
payload = json.dumps(payload)

#print(payload)            
url = "http://localhost:9200/document/_search"
response = requests.request("GET", url, data=payload, headers=headers)
response_dict_data = json.loads(str(response.text))
print(response_dict_data['hits']['hits'][0]['_source'].keys())
'''

from flask import Blueprint,render_template,request,jsonify
import requests,json

from haystack import Finder
from haystack.database.elasticsearch import ElasticsearchDocumentStore

#from haystack.indexing.cleaning import clean_wiki_text
#from haystack.indexing.io import write_documents_to_db, fetch_archive_from_http
from haystack.reader.farm import FARMReader
from haystack.retriever.elasticsearch import ElasticsearchRetriever
from haystack.utils import print_answers

#define reader and retriever
document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")
            # Difference 3: Use the native Elasticsearch implementation of BM25 as a Retriever
retriever = ElasticsearchRetriever(document_store=document_store)

            # Init reader & and use Finder to get answer (same as in Tutorial 1)
reader = FARMReader(model_name_or_path="/home/sebastian/SideProject/QA/MLQA_V1/bert-base-german-dbmdz-cased-MLQA/data/saved_models/bert-base-german-dbmdz-cased-MLQA",use_gpu=-1)
finder = Finder(reader=reader, retriever=retriever)





# creating a Blueprint class
search_blueprint = Blueprint('search',__name__,template_folder="templates")

search_term = ""


headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
}

@search_blueprint.route("/",methods=['GET','POST'],endpoint='index')
def index():
    if request.method=='GET':
        res ={
	            'hits': {'total': 0, 'hits': []}
             }
        return render_template("index_dev.html",res=res)
    elif request.method =='POST':
        if request.method == 'POST':
            print("-----------------Calling search Result----------")
            search_term = request.form["input"]
            print("Search Term:", search_term)
            payload = {
                "query": {
                    "query_string": {
                        "analyze_wildcard": True,
                        "query": str(search_term),
                        "fields": ["name", "text", "_score"]
                    }
                },
                "size": 50,
                "sort": [

                ]
            }
            payload = json.dumps(payload)
            url = "http://localhost:9200/document/_search"
            response = requests.request("GET", url, data=payload, headers=headers)
            response_dict_data = json.loads(str(response.text))
            print(response_dict_data['hits']['hits'])
            
            #convert results in a harmonized format
            res = []
            for hit in response_dict_data['hits']['hits']:
                dict_res = {'answer':hit['_source']['name'], # TODO: change;this is actually the title of the file
                            'context': hit['_source']['text'],
                            'score': hit['_score'],
                            'probability': -1 # TODO: check how to implement probalilty or use finder(reader=none, retriever=retriever)?
                }
                res.append(dict_res)

            count_hits = response_dict_data['hits']['total']['value']
            return render_template('index_dev.html',
                                    res=res, 
                                    search_term= search_term,
                                    count_hits=count_hits)


@search_blueprint.route("/transformer_search",methods=['GET','POST'],endpoint='transformer_search')
def transformer_search():
    if request.method=='GET':
        res ={
	            'hits': {'total': 0, 'hits': []}
             }
        return render_template("index_dev.html",res=res)
       
    elif request.method =='POST':

        if request.method == 'POST':
            print("-----------------Calling search Result----------")
            search_term = request.form["input_transformer"]
            print("Search Term:", search_term)
            res_transformer = finder.get_answers(question=search_term, top_k_retriever=10, top_k_reader=5)
            print(res_transformer)
            dict_res = [] #TODO: dict_res musss nich erstellt, werden da im Jinja template ebenfalls extrahiert/iteriert werden kann
        
            res = []
            for answer in res_transformer['answers']:
                dict_res = {'answer': answer['answer'],
                            'context': answer['context'],
                            'score': answer['score'],
                            'probability': answer['probability']
                }
                res.append(dict_res)
            print_answers(res_transformer, details="medium")


            count_hits = -1 #TODO: implement count of results
            return render_template('index_dev.html',
                                    res=res,
                                    search_term= search_term,
                                    count_hits=count_hits)
    

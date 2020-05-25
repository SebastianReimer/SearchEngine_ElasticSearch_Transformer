import requests
import json

def check_if_index_is_present(url):
    response = requests.request("GET", url, data="")
    json_data = json.loads(response.text)
    return json_data


if __name__ == "__main__":
    url = "http://localhost:9200/_template/search_engine_template/"
    response = requests.request("GET", url, data="")
    if(len(response.text)>2):
        print("1. Deleted template: search_engine_template")
        response_delete = requests.request("DELETE", url)
    payload = {
          "template": "document",
          "settings": {
            "number_of_shards": 1
          },
			"mappings": {
				"_source":{
					"enabled": True
				},
					
				"properties":
					{"document_id": {"type":"integer"},
						"name":{"type":"text"},
						"text":{"type":"text"}
					}
			}
    }
    payload = json.dumps(payload)
    headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
    response = requests.request("PUT", url, data=payload, headers=headers)
    
    if (response.status_code == 200): # if http-request was successful
        print("2. Created a new template: search_engine_template")
    print("search_engine_template response.text:")
    print(response.text)

    url = "http://localhost:9200/document"
    json_data = check_if_index_is_present(url)

    if(not 'error' in json_data):
        print("3. Deleted an index: document")
        response = requests.request("DELETE", url)

    response = requests.request("PUT", url)
    if (response.status_code == 200):
        print("4. Created an index: document")





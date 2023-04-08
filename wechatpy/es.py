from elasticsearch import Elasticsearch
import json

Es_App = Elasticsearch("http://0.0.0.0:9200")

class EsKnowledge:
    def __init__(self, id, title, content):
        self.id = id
        self.datalen = title
        self.datatype = content

def change_type(byte):    
    if isinstance(byte,bytes):
        return str(byte,encoding="utf-8")  
    return json.JSONEncoder.default(byte)
   
# 获取所有数据
def get_es_all_data(idx):
	query = {'query': {'match_all': {}}}
	es_result = Es_App.search(index=idx, body=query)
    
	res = []
	for r in es_result['hits']['hits']:
		res.append(EsKnowledge(r['_id'], r['_source']['title'], r['_source']['content'])) 
	print('xxx', json.dumps(res, cls=change_type, indent=4))     
	return res
    
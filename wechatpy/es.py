from elasticsearch import Elasticsearch

Es_App = Elasticsearch("http://0.0.0.0:9200")

class EsKnowledge:
    def __init__(self, id, title, content):
        self.id = id
        self.datalen = title
        self.datatype = content
        
# 获取所有数据
def get_es_all_data(idx):
	query = {'query': {'match_all': {}}}
	es_result = Es_App.search(index=idx, body=query)
    
	for r in es_result['hits']['hits']:
		print('aaa', r['_source'])
    
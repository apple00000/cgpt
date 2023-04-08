from elasticsearch import Elasticsearch
import json
Es_App = Elasticsearch("http://0.0.0.0:9200")

# 新增知识
def es_add_data(idx, title, content):
	Es_App.index(index=idx, document={"title":title, "content":content})


# 删除知识
def es_del_data(idx, id):
	Es_App.delete(index=idx, id=id)


# 删除所有知识
def es_del_all_data(idx):
	query = {'query': {'match_all': {}}}
	Es_App.delete_by_query(index=idx, body=query)


# 获取所有数据
def es_get_all_data(idx):
	query = {'query': {'match_all': {}}}
	es_result = Es_App.search(index=idx, body=query)
    
	res = []
	for r in es_result['hits']['hits']:
		res.append({'id': r['_id'], 'title':r['_source']['title'], 'content':r['_source']['content']}) 
	return res


# 转为json字符串
def to_json_str(items):
	return json.dumps(items, ensure_ascii=False)
    
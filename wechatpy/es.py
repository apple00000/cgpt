from elasticsearch import Elasticsearch
import json
from loguru import logger

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
	logger.info('[es_get_all_data] es_result:{}'.format(es_result))
    
	return to_local_struct(es_result)


# 查询数据
def es_query(idx, str):
	query = {'query': 
	  {'bool':
    	{'should':
      		[{'match': {'title':{'query':str, 'boost':1}}},
	 		 {'match': {'content':{'query':str, 'boost':1}}}
	 		]
	 	}
	  }
	 }
	es_result = Es_App.search(index=idx, body=query)
	print("xxx1", es_result)
	return to_local_struct(es_result)


# 转为json字符串
def to_json_str(items):
	return json.dumps(items, ensure_ascii=False)


# 转为结构体
def to_local_struct(es_result):
	res = []
	for r in es_result['hits']['hits']:
		res.append({'id': r['_id'], 'title':r['_source']['title'], 'content':r['_source']['content']}) 
	return res
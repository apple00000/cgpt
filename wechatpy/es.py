from elasticsearch import Elasticsearch
import json
from loguru import logger

Es_App = Elasticsearch("http://0.0.0.0:9200")

def is_sys_command(command):
	command = str(command)
	if command.startswith('&&'):
		return True
	return False


# 被动回复检查
def sys_command(idx, command):
	command = str(command)
	logger.info('get_sys_command... {}'.format(command))

	if command.startswith('&&查询所有模型'):
		logger.info("[查询所有模型] command:{}".format(command))
		es_res = es_get_all_data(idx)
		logger.info("[查询所有模型] es_res:{}".format(es_res))
		res = ""
		for r in es_res:
			res += r['id'] + ' ' + r['title'] + '\n'
		if res=="":
			res = "无数据"

		return res

	if command.startswith('&&查询单个模型'):
		command = command.replace('&&查询单个模型', '')
		command = command.strip()
		if command=="":
			return "模型id不能为空"
		
		es_res = es_query_id(idx, command)
		res = ""
		for r in es_res:
			res += r['id'] + '\n' + r['title'] + '\n' + r['content'] + '\n'
		if res=="":
			res = "无数据"
		return res
	
	if command.startswith('&&添加模型'):
		command = command.replace('&&添加模型', '')
		command = command.strip()
		items = command.split('\n')
		if len(items)<2:
			return "模型需要包含标题和内容，第一行是标题，后面是内容"
		title = items[0]
		content = '\n'.join(items[1:])
		es_add_data(idx, title, content)
		return "ok"

	if command.startswith('&&删除单个模型'):
		command = command.replace('&&删除单个模型', '')
		command = command.strip()
		if command=="":
			return "模型id不能为空"
		
		es_res = es_del_data(idx, command)
		return es_res
	
	if command.startswith('&&删除所有模型'):
		es_del_all_data(idx)
		return "ok"
	
	return "不是系统命令"


# 新增知识
def es_add_data(idx, title, content):
	res = Es_App.index(index=idx, document={"title":title, "content":content})
	logger.info('[es_add_data] res:{}'.format(res))

# 删除知识
def es_del_data(idx, id):
	try:
		Es_App.delete(index=idx, id=id)
		return "ok"
	except:
		return "id不存在"


# 删除所有知识
def es_del_all_data(idx):
	query = {'query': {'match_all': {}}}
	Es_App.delete_by_query(index=idx, body=query)


# 获取所有数据
def es_get_all_data(idx):
	query = {'query': {'match_all': {}}}
	es_result = Es_App.search(index=idx, body=query)
	logger.info('[es_get_all_data] es_result:{}'.format(es_result))
    
	return to_local_struct_id_title(es_result)


# 获取私域知识
def es_self_knowledge(idx, str):
	res = ""
	local_res = es_query_str(idx, str)
	for r in local_res:
		tmp = res + r['title']+'\n'+r['content']+'\n\n'
		if len(tmp)>1000:
			break
		res = tmp
	
	logger.info('[es_self_knowledge] str:{}, res:{}'.format(str, res))
	return res


# 查询数据
def es_query_str(idx, str):
	query = {'query': 
	  {'bool':
    	{'should':
      		[{'match': {'title':{'query':str, 'boost':2}}},
	 		 {'match': {'content':{'query':str, 'boost':1}}}
	 		]
	 	}
	  }
	}
	es_result = Es_App.search(index=idx, body=query)
	logger.info('[es_query_str] query:{}, es_result:{}'.format(str, es_result))

	return to_local_struct(es_result)


# 查询数据
def es_query_id(idx, id):
	query = {'query': {'match': {'_id': id}}}
	es_result = Es_App.search(index=idx, body=query)
	logger.info('[es_query_id] query:{}, es_result:{}'.format(str, es_result))

	return to_local_struct(es_result)


# 转为json字符串
def to_json_str(items):
	return json.dumps(items, ensure_ascii=False)


# 转为结构体，不含content,score
def to_local_struct_id_title(es_result):
	res = []
	for r in es_result['hits']['hits']:
		res.append({'id': r['_id'], 'title':r['_source']['title']}) 
	return res


# 转为结构体
def to_local_struct(es_result):
	res = []
	for r in es_result['hits']['hits']:
		res.append({'id': r['_id'], 'score':r['_score'] ,'title':r['_source']['title'], 'content':r['_source']['content']}) 
	return res
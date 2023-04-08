from elasticsearch import Elasticsearch

# 默认host为localhost,port为9200.但也可以指定host与port
es = Elasticsearch("http://0.0.0.0:9200")
 
# 插入数据,index，doc_type名称可以自定义，id可以根据需求赋值,body为内容
# es.index(index="index", document={"title":"python", "content":"深圳"})

query = {'query': {'match_all': {}}}# 查找所有文档
query_name = {'query': {'match': {'name':'深' }}}# 查找所有文档

result = es.search(index="index", body=query_name)
print('result', result)# 返回第一个文档的内容


query_name_2 = {'query': {'match': {'name':'上' }}}# 查找所有文档

result2 = es.search(index="index", body=query_name_2)
print('result2', result2)# 返回第一个文档的内容

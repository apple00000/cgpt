from elasticsearch import Elasticsearch

# 默认host为localhost,port为9200.但也可以指定host与port
es = Elasticsearch("http://0.0.0.0:9200")
 
# 插入数据,index，doc_type名称可以自定义，id可以根据需求赋值,body为内容
es.index(index="index", document={"title":"python", "content":"深圳"})
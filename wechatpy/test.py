import es

file_object = open("刚需探房.txt",'r')
all_the_text = file_object.read()
fs = all_the_text.split('\n\n\n')

content_index = 1
for f in fs:
	f2s = f.split('\n')
	if len(f2s)!=4:
		continue
	title = f2s[0].replace('【标题】','')
	content = f2s[3].replace('【内容】','')

	while len(content)>1000:
		tmp = content[:1000]
		content = content[1000:]

		print("xxx1", title+"("+str(content_index)+")")
		print("xxx2", tmp)
		content_index+=1
		es.es_add_data("index", title, tmp)

	print("xxx1", title+"("+str(content_index)+")")
	print("xxx2", content)
	content_index=1
	es.es_add_data("index", title, content)
	



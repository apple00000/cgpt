import es
import os

# 遍历文件夹
def get_files_from_dir(dir):
	if not os.path.exists(dir):
		return ''
	file_paths = []
	for root, directories, files in os.walk(dir):
		for filename in files:
			filepath = os.path.join(root, filename)
			file_paths.append(filepath)

	return file_paths


def save_data(path, es_index):
	file_object = open(path, 'r')
	all_the_text = file_object.read()
	fs = all_the_text.split('\n\n')

	for f in fs:
		f2s = f.split('\n')
		if len(f2s)!=2:
			continue
		title = f2s[0]
		content = f2s[1]
		es.es_add_data(es_index, title, content)
	

if __name__ == '__main__': 
	save_data('./刚需探房_总结.txt', '1')
	# file_list = get_files_from_dir('./mscyw')
	# for file in file_list:
	# 	save_data(file, '2')
import requests
from loguru import logger
import json
import uuid
import time


def get_ai(openid, content, system_desc, server):
	logger.info("[get_ai] {} {}".format(openid, content))

	post_dict = {}
	post_dict["session"] = openid
	post_dict["query"] = content
	post_dict["system"] = system_desc
	post_dict["server"] = server

	j = json.dumps(post_dict)

	res = requests.post(url='http://34.28.10.140:10001', data=j)
	logger.info("[ai_res] {}".format(res.text))

	return res.text


if __name__ == '__main__':
	file_object = open("刚需探房.txt",'r')
	all_the_text = file_object.read()
	fs = all_the_text.split('\n\n\n')

	user = str(uuid.uuid4())
	content_index = 1

	file2 = open('刚需探房_总结.txt', 'w')

	for f in fs:
		f2s = f.split('\n')
		if len(f2s)!=4:
			continue
		title = f2s[0].replace('【标题】','')
		content = f2s[3].replace('【内容】','')

		while len(content)>3000:
			content = content[:3000]

		s = '帮我把之前的内容总结为400-500字左右的概述：\n\n'+content
		
		r = get_ai(user, s ,'', '')
		print(r)
		file2.write(title+'\n'+r+'\n\n')
		time.sleep(10)

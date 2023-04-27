import utils
from loguru import logger

# 推荐列表
recommend_info = []

# 加载推荐文件
def load_recommend_file():
	global recommend_info

	f0 = utils.read_file("./福州购房宝典.txt")
	print("[load_recommend_file] ", f0)
    
	f1 = f0.split('\n')
	for f2 in f1:
		item = f2.split('\t')
		title = item[0]
		kw = item[1].split(' ')
		price = item[2]
		detail = item[3]
		url = item[4]
		v = {
			"title":title,
			"kw":kw,
			"price":price,
			"detail":detail,
			"url":url
		}
		recommend_info.append(v)

	logger.info("load_recommend_file done {}".format(recommend_info))
	

# 根据关键词给出推荐商品
def match_product(s):
	data = ''
	res = []

	for r in recommend_info:
		for word in r['kw']:
			if word in s:
				res.append(r)
				break
	
	if len(res)==0:
		return ""

	data += "回答内容引导用户购买以下商品：\n"
	index = 1
	for r in res:
		item = str(index)+'）'+r['title']+'   '+r['price']+'元   '+r['url']+'   '+r['detail']
		index+=1
		data += item+"\n"
		
	return data



if __name__ == '__main__':
	load_recommend_file()

	print(match_product('如何购房'))
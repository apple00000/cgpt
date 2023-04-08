from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from flask import Flask, request
from wechatpy import parse_message
from gevent import pywsgi
import json
from wechatpy import WeChatClient
import requests
from loguru import logger
import xmltodict
from wechatpy.utils import to_text
from threading import Thread
import es

cache = {}
system_desc = ""
client = WeChatClient('wx02ebfbc6b41b8693', '56cedd8e54f1c184b15f57bbb4344928')
client_2 = WeChatClient('wx9789602164af57fd', '704b040fe51a750af281d9f39a8fd88a')

app = Flask(__name__) #实例化Flask对象app

@app.route('/wechat_msg', methods=['GET', 'POST']) #app中的route装饰器
def hello_world():
    token = "zpsf01234560123456"
    signature = request.args['signature']
    timestamp = request.args['timestamp']
    nonce = request.args['nonce']
    openid = request.args['openid']

    # 去重，微信公众号会发三次
    if openid+timestamp in cache:
        logger.info("[cache] {} {}".format(openid, timestamp))
        return ""
    cache[openid+timestamp] = True

    raw_data = request.data
    logger.info("[get_user] {} {} {} {} {}".format(signature, timestamp, nonce, openid, raw_data))

    msg = parse_message(raw_data)
    msg = xmltodict.parse(to_text(raw_data))['xml']
    logger.info("[get_msg] {}".format(msg))

    if msg['MsgType']!='text':
        logger.info('[msgtype] {}'.format(msg['MsgType']))
        return ""
    
    content = msg['Content']
    logger.info("[get_msg_content] {}".format(content))

    self_knowledge = es.es_self_knowledge("index", content)

    t=Thread(target=get_ai, args=(openid, content, system_desc+'\n'+self_knowledge, client))
    t.start()

    return ""


@app.route('/wechat_msg_2', methods=['GET', 'POST']) #app中的route装饰器
def hello_world_2():
    logger.info("wechat_msg_2...")
    token = "zpsf01234560123456"
    signature = request.args['signature']
    timestamp = request.args['timestamp']
    nonce = request.args['nonce']

    # 验证
    # echostr = request.args['echostr']
    # logger.info("[check] {} {} {} {}".format(signature, timestamp, nonce, echostr))
    # try:
    #     check_signature(token, signature, timestamp, nonce)
    #     logger.info("check ok")
    #     return echostr
    # except InvalidSignatureException: 
    #     logger.info("check fail")    
    #     return ""
    
    openid = request.args['openid']
    
    # 去重，微信公众号会发三次
    if openid+timestamp in cache:
        logger.info("[cache] {} {}".format(openid, timestamp))
        return ""
    cache[openid+timestamp] = True

    raw_data = request.data
    logger.info("[get_user] {} {} {} {} {}".format(signature, timestamp, nonce, openid, raw_data))

    msg = parse_message(raw_data)
    msg = xmltodict.parse(to_text(raw_data))['xml']
    logger.info("[get_msg] {}".format(msg))

    if msg['MsgType']!='text':
        logger.info('[msgtype] {}'.format(msg['MsgType']))
        return ""
    
    content = msg['Content']
    logger.info("[get_msg_content] {}".format(content))

    t=Thread(target=get_ai, args=(openid, content, "", client_2))
    t.start()

    return ""


@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    title = request.args['title']
    if (len(title))>30:
        return ""
    if (len(content))>500:
        return "content不能超过500个字符"

    content = request.args['content']
    logger.info("[add_data] title:{}, content:{}".format(title, content))
    es.es_add_data("index", title, content)
    return "ok"


@app.route('/del_all_data', methods=['GET', 'POST'])
def del_all_data():
    logger.info("[del_all_data]")
    es.es_del_all_data("index")
    return "ok"
    

@app.route('/del_data', methods=['GET', 'POST'])
def del_data():
    id = request.args['id']
    logger.info("[del_data] id:{}".format(id))
    try:
        es.es_del_data("index", id)
    except:
        return "未删除成功"
    return "ok"


@app.route('/get_all_data', methods=['GET', 'POST'])
def get_all_data():
    logger.info("[get_all_data]")
    r = es.es_get_all_data("index")
    return es.to_json_str(r)


# 加载公共知识
def load_system_desc():
    global system_desc
    system_desc = read_file("./system_desc.txt")
    print("[load_system_desc] ", system_desc)

def read_file(path):
    with open(path, mode='r', encoding='utf-8') as f:
        return f.read()


# 调用openai接口
def get_ai(openid, content, system_desc, c):
    logger.info("[get_ai] {} {}".format(openid, content))

    post_dict = {}
    post_dict["session"] = openid
    post_dict["query"] = content
    post_dict["system"] = system_desc
    j = json.dumps(post_dict)

    res = requests.post(url='http://34.28.10.140:10001', data=j)
    logger.info("[ai_res] {}".format(res.text))

    res_code = c.message.send_text(openid, res.text)
    logger.info("[send_text] {}".format(res_code))


if __name__ == '__main__':  
    load_system_desc()

    server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    logger.info("server start...")
    server.serve_forever()
    
    

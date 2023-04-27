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
from wechatpy.replies import TextReply
import base64
import qiye_code
import utils
import recommend

cache = {}
system_desc = ""

# 测试公众号
client_2 = WeChatClient('wx9789602164af57fd', '704b040fe51a750af281d9f39a8fd88a')

app = Flask(__name__) #实例化Flask对象app

# 祖平说房 测试号
@app.route('/wechat_msg', methods=['GET', 'POST']) #app中的route装饰器
def hello_world():
    zupingshuofang('wx02ebfbc6b41b8693', '56cedd8e54f1c184b15f57bbb4344928')
    return ""


# 祖平说房
@app.route('/wechat_msg_zpsf', methods=['GET', 'POST']) #app中的route装饰器
def hello_world_zpsf():
    logger.info("hello_world_zpsf ...")

    # # 验证服务器配置
    # token = "zpsf01234560123456"
    # signature = request.args['signature']
    # timestamp = request.args['timestamp']
    # nonce = request.args['nonce'] 
    # echostr = request.args['echostr']
    # logger.info("[check] {} {} {} {}".format(signature, timestamp, nonce, echostr))
    # try:
    #     check_signature(token, signature, timestamp, nonce)
    #     logger.info("check ok")
    #     return echostr
    # except InvalidSignatureException: 
    #     logger.info("check fail")    
    #     return ""

    zupingshuofang('wxc1cc92da11178815', '7f15a75d60af6f5bfdb303b13fb0b4b0')
    return ""


# 祖平说房公众号逻辑
def zupingshuofang(key, value):
    client = WeChatClient(key, value)

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

    # 系统命令
    if es.is_sys_command(content):
        sys_res = es.sys_command("index", content)
        send_text(openid, sys_res, client)
        return ""
    
    self_knowledge = ""
    # self_knowledge = es.es_self_knowledge("index", content)

    # 推荐附加
    rec = recommend.match_product(content)
    logger.info("match_product {}".format(rec))

    t=Thread(target=get_ai, args=(openid, content, system_desc+'\n'+self_knowledge+'\n'+rec, client, ""))
    t.start()


# 私有号
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

    t=Thread(target=get_ai, args=(openid, content, "", client_2, ""))
    t.start()

    return ""


# 祖平说房 企业微信
@app.route('/wechat_msg_qiye', methods=['GET', 'POST']) #app中的route装饰器
def wechat_msg_qiye():
    logger.info("wechat_msg_qiye...")
    token = "BioALSjOF4fadlywjXj1zWb"
    msg_signature = request.args['msg_signature']
    timestamp = request.args['timestamp']
    nonce = request.args['nonce']

    # 验证
    echostr = request.args['echostr']
    logger.info("[wechat_msg_qiye] check {} {} {} {}".format(msg_signature, timestamp, nonce, echostr))

    msg = qiye_code.de_echostr(echostr)
    logger.info("[wechat_msg_qiye] msg {} {}".format(msg, str(msg)))

    return ""

    
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

    t=Thread(target=get_ai, args=(openid, content, "", client_2, ""))
    t.start()

    return ""


@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    title = request.args['title']
    content = request.args['content']
    if (len(title))>30:
        return ""
    if (len(content))>500:
        return "content不能超过500个字符"

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
    system_desc = utils.read_file("./system_desc.txt")
    print("[load_system_desc] ", system_desc)


# 调用openai接口
def get_ai(openid, content, system_desc, c, add_text):
    logger.info("[get_ai] {} {}".format(openid, content))

    post_dict = {}
    post_dict["session"] = openid
    post_dict["query"] = content
    post_dict["system"] = system_desc

    logger.info("system_desc : {}".format(system_desc))

    j = json.dumps(post_dict)

    res = requests.post(url='http://34.28.10.140:10001', data=j)
    logger.info("[ai_res] {}".format(res.text))

    res_code = c.message.send_text(openid, res.text+add_text)
    logger.info("[send_text] {}".format(res_code))


# 主动发送消息
def send_text(openid, content, c):
    c.message.send_text(openid, content)


if __name__ == '__main__':  
    load_system_desc()
    recommend.load_recommend_file()

    server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    logger.info("server start...")
    server.serve_forever()
    
    

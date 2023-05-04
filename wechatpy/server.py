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
import time

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

    msgType = msg['MsgType']
    
    # 文字
    if msgType == 'text':
        content = msg['Content']
        logger.info("[get_msg_content] {}".format(content))

        zfsp_auto_reply(client, openid, content)

        # 菜单消息
        # if content=='你好':
        #     d = {"head_content": "可以点击提问：", "list":[{"id":"101", "content":"祖平说房提供什么服务？"}], "tail_content":""}
        #     res_code = client.message.send_msg_menu(openid, d)
        #     return ''


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

        t=Thread(target=get_ai, args=(openid, content, system_desc+'\n'+self_knowledge, client, '\n'+rec))
        t.start()

    # 事件
    elif msgType == 'event':
        event = msg['Event']
        # 关注
        if event == 'subscribe':
            s = '您好，感谢您的关注与支持！【祖平说房】,专注家庭房产配置，为您提供一站式房产配置顾问服务。\n您可直接在对话框输入内容，我们智能助手 将24小时为您提供线上服务。\n如果您有需要预约祖平老师线下咨询，请识别二维码或直接添加微信：18960709019'
            res_code = client.message.send_text(openid, s)
            logger.info("[send_text] text {}".format(res_code))
            res_code = client.message.send_image(openid, 'PFrQoA4lwFQr5sLE_F4HjEqP13GQwNOh6SswuzYqt3389S2r6GwpM0ZjeITtUSeX')
            logger.info("[send_text] image {}".format(res_code))

    else:
        logger.info('[msgtype] {}'.format(msg['MsgType']))
        return ""
    

# 祖平说房自动回复 
def zfsp_auto_reply(client, openid, str):
    if '人才房' in str:
        res_code = client.message.send_text(openid, '推荐阅读这篇公众号文章【重磅！福州发放政策“大礼包”！涉及公租房、人才住房……】\nhttps://mp.weixin.qq.com/s?__biz=MzI2ODc4NTYyMw==&mid=2247487860&idx=1&sn=57c2965aa48c13625f22527c90bea25a&chksm=eaeb13ccdd9c9adadbb6a51cb977349b711ab99fb39c51258b8960d751a7fecdcdbc90641697&token=1846401951&lang=zh_CN#rd')
        logger.info("[send_text] text {}".format(res_code))

    if '地铁' in str:
        res_code = client.message.send_text(openid, '推荐阅读这篇公众号文章【提前谋划6条线路，福州最新地铁建设规划曝光】\nhttps://mp.weixin.qq.com/s?__biz=MzI2ODc4NTYyMw==&mid=2247488076&idx=1&sn=ebd805fbd63705f2426c436a5c544138&chksm=eaeb10f4dd9c99e25b5cf8422bca034287c356d6b1dec17ee2baa7e16e826245948320380d9c&token=1846401951&lang=zh_CN#rd')
        logger.info("[send_text] text {}".format(res_code))

    if '落户' in str:
        res_code = client.message.send_text(openid, '推荐阅读这篇公众号文章【福州落户最全指南，拿走不谢】\nhttps://mp.weixin.qq.com/s?__biz=MzI2ODc4NTYyMw==&mid=2247484588&idx=1&sn=ba3baaaeb63599f64dda66dc7998c89c&chksm=eaeb0614dd9c8f022a45e00a1197b8f14cfb855c3e0d1da68e592166eb699244243f072b70c7&token=1846401951&lang=zh_CN#rd')
        logger.info("[send_text] text {}".format(res_code))

    if '税收' in str:
        res_code = client.message.send_text(openid, '推荐阅读这篇公众号文章【怎么判定名下房产套数？买卖房屋需缴纳多少税费？福州房产交易最全指南】\nhttps://mp.weixin.qq.com/s?__biz=MzI2ODc4NTYyMw==&mid=2247486998&idx=1&sn=21a942d77ec508281e23ca3bd8861e5f&chksm=eaeb0caedd9c85b8b5d2575626424b4f52c4543022f3d333a7520e2f3833f8a404595222a0f4&token=1846401951&lang=zh_CN#rd')
        logger.info("[send_text] text {}".format(res_code))

    if '直播' in str:
        res_code = client.message.send_text(openid, '【直播】\n福州楼市政策，搜索抖音号：福州祖平说房；\n楼市干货直播，每周二、四晚9-12点\n1.搜索抖音号：福州祖平说房【直播号丨佑居】\n2.点击链接：https://apptwzlpzwb4621.h5.xiaoeknow.com')
        logger.info("[send_text] text {}".format(res_code))

    if '微信' in str:
        res_code = client.message.send_image(openid, 'PFrQoA4lwFQr5sLE_F4HjBermVpDQ4GqoeqghzeD6plj7lp1XfqQmvEgDpG_hJyO')
        logger.info("[send_text] image {}".format(res_code))

    if '地图' in str:
        res_code = client.message.send_text(openid, '【福州楼市地图】点击下方链接即可领取\nhttps://apptwzlpzwb4621.h5.xiaoeknow.com/p/course/text/i_61518c0fe4b0448bf65ddf09')
        logger.info("[send_text] text {}".format(res_code))


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
    
    

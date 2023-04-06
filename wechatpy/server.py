from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from flask import Flask, request
from wechatpy import parse_message
from gevent import pywsgi
import json
from wechatpy import WeChatClient
import requests
from loguru import logger


cache = {}

client = WeChatClient('wx02ebfbc6b41b8693', '56cedd8e54f1c184b15f57bbb4344928')

app = Flask(__name__) #实例化Flask对象app

@app.route('/wechat_msg', methods=['GET', 'POST']) #app中的route装饰器
def hello_world():
    token = "zpsf01234560123456"
    signature = request.args['signature']
    timestamp = request.args['timestamp']
    nonce = request.args['nonce']
    openid = request.args['openid']

    # 去重
    if openid+timestamp in cache:
        logger.info("[cache] {} {}".format(openid, timestamp))
        return ""
    cache[openid+timestamp] = True

    raw_data = request.data
    logger.info("[get_user] {} {} {} {}".format(signature, timestamp, nonce, openid))
    msg = parse_message(raw_data)
    logger.info("[get_msg] {}".format(msg))

    if msg.msgtype != 'text':
        logger.info('[msgtype] {}'.format(msg.msgtype))
        return ""
    
    content = msg.content
    logger.info("[get_msg_content] {}".format(content))

    res = requests.get(url='http://34.28.10.140:10001', params={"session":openid, "query": content})
    logger.info("[ai_res] {}".format(res.text))

    res_code = client.message.send_text(openid, res.text)
    logger.info("[send_text] {}".format(res_code))

    # try:
    #     check_signature(token, signature, timestamp, nonce)
    # except InvalidSignatureException:
    #     print("xxx3")
    #     pass

    return ""

if __name__ == '__main__':    
    server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    logger.info("server start...")
    server.serve_forever()
    

def read_file(path):
    with open(path, mode='r', encoding='utf-8') as f:
        return f.read()
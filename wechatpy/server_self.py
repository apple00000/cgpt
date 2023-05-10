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

app = Flask(__name__) #实例化Flask对象app

@app.route('/ai_simple', methods=['GET', 'POST']) #app中的route装饰器
def ai_simple():
    logger.info("[ai_simple]")   
    content = request.args['content']
    return ""


# 调用openai接口
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
    server = pywsgi.WSGIServer(('0.0.0.0', 10002), app)
    logger.info("server self start...")
    server.serve_forever()
    
    

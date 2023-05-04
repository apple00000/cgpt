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
# import es
# from wechatpy.replies import TextReply
# import base64
# import qiye_code
# import utils
# import recommend
# import time

cache = {}
system_desc = ""

app = Flask(__name__) #实例化Flask对象app


# 祖平说房
@app.route('/douyin_airen', methods=['GET', 'POST']) #app中的route装饰器
def douyin_airen():
    logger.info("douyin_airen ...")

    # 验证服务器配置
    token = "123456123456"
    signature = request.args['signature']
    timestamp = request.args['timestamp']
    nonce = request.args['nonce'] 
    msg = request.args['msg'] 
    echostr = request.args['echostr']
    logger.info("[check] {} {} {} {} {}".format(signature, timestamp, msg, nonce, echostr))
    
    return echostr



if __name__ == '__main__':  
    # server = pywsgi.WSGIServer(('0.0.0.0', 443), app, None, "default", "default", "defalut",None,None, ssl_context='adhoc')
    # logger.info("server start...")
    # server.serve_forever()
    app.run(host="0.0.0.0", port=443, ssl_context=('server.crt', 'server.key'))
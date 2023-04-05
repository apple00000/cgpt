from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from flask import Flask, request
from wechatpy import parse_message
from gevent import pywsgi
import json
from wechatpy import WeChatClient

client = WeChatClient('appid', 'secret')
app = Flask(__name__) #实例化Flask对象app

@app.route('/wechat_msg', methods=['GET', 'POST']) #app中的route装饰器
def hello_world():
    print("xxx1")
    token = "zpsf01234560123456"
    signature = request.args['signature']
    timestamp = request.args['timestamp']
    nonce = request.args['nonce']
    openid = request.args['openid']
    raw_data = request.data
    print("xxx2", signature, timestamp, nonce, openid, raw_data)

    res = client.message.send_text(openid, '222')
    print("xxx3", res)

    msg = parse_message(raw_data)
    print("xxx4", msg)
    
    # try:
    #     check_signature(token, signature, timestamp, nonce)
    # except InvalidSignatureException:
    #     print("xxx3")
    #     pass

    return ""

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    print("server start...")
    server.serve_forever()
    

def read_file(path):
    with open(path, mode='r', encoding='utf-8') as f:
        return f.read()
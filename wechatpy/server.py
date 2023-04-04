from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from flask import Flask, request
from gevent import pywsgi
import json

app = Flask(__name__) #实例化Flask对象app

@app.route('/', methods=['GET']) #app中的route装饰器
def hello_world():
    token = "zpsf01234560123456"
    signature = request.args['signature']
    timestamp = request.args['timestamp']
    nonce = request.args['nonce']
    echostr = request.args['echostr']
 
    try:
        check_signature(token, signature, timestamp, nonce)
    except InvalidSignatureException:
        pass

    return echostr

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    print("server start...")
    server.serve_forever()
    

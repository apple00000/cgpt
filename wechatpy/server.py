from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from flask import Flask, request
from gevent import pywsgi
import json

app = Flask(__name__) #实例化Flask对象app

@app.route('/wechat_msg', methods=['GET', 'POST']) #app中的route装饰器
def hello_world():
    print("xxx1")
    token = "zpsf01234560123456"
    signature = request.args['signature']
    timestamp = request.args['timestamp']
    nonce = request.args['nonce']
    print("xxx2", signature, timestamp, nonce)
 
    try:
        check_signature(token, signature, timestamp, nonce)
    except InvalidSignatureException:
        pass

    return "222"

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    print("server start...")
    server.serve_forever()
    

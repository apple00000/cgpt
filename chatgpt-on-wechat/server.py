import config
from bot.chatgpt.chat_gpt_bot import ChatGPTBot
from plugins import *
from bridge.context import *
from flask import Flask, request
from gevent import pywsgi
import json
from loguru import logger

app = Flask(__name__) #实例化Flask对象app

@app.route('/', methods=['GET', 'POST']) #app中的route装饰器
def hello_world():
    session = request.args['session']
    query = request.args['query']
    system = request.args['system']

    logger.info("[hello_world] session {}, query {}, system{}".format(session, query, system))
    bot_context['session_id'] = session
    r = bot.reply(query, system, bot_context)

    return r.content

if __name__ == '__main__':
    config.load_private_desc()
    config.load_config()
    config.load_system_desc()
    
    bot = ChatGPTBot()
    bot_context = Context(
        type = ContextType.TEXT
	)
    
    server = pywsgi.WSGIServer(('0.0.0.0', 10001), app)
    print("server start...")
    server.serve_forever()
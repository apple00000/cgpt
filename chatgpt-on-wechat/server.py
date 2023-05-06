import config
from bot.chatgpt.chat_gpt_bot import ChatGPTBot
from plugins import *
from bridge.context import *
from flask import Flask, request
from gevent import pywsgi
import json
import openai
from loguru import logger

app = Flask(__name__) #实例化Flask对象app

@app.route('/', methods=['GET', 'POST']) #app中的route装饰器
def hello_world():
    j = json.loads(request.data)
    session = j['session']
    query = j['query']
    system = j['system']
    # server = j['server']

    # logger.info("[hello_world] session {}, query {}, system {}, server {}".format(session, query, system, server))

    # 根据不同服务重置key
    # if server=='' or server=='0' or server==None:
    #     openai.api_key = config.conf().get('open_ai_api_key')
    # if server=='1':
    #     openai.api_key = config.conf().get('open_ai_api_key_1')

    logger.info("api_key {}".format(openai.api_key))

    bot_context['session_id'] = session
    r = bot.reply(query, system, bot_context)

    return r.content

if __name__ == '__main__':
    # config.load_private_desc()
    config.load_config()
    # config.load_system_desc()
    
    bot = ChatGPTBot()
    bot_context = Context(
        type = ContextType.TEXT
	)
    
    server = pywsgi.WSGIServer(('0.0.0.0', 10001), app)
    print("server start...")
    server.serve_forever()
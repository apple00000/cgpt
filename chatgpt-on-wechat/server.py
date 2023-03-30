import argparse
import json
import urllib
from http.server import HTTPServer, BaseHTTPRequestHandler
import config
from channel import channel_factory
from common.log import logger
from bot.chatgpt.chat_gpt_bot import ChatGPTBot
from plugins import *
from bridge.context import *

host = ('127.0.0.1', 10001)

class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        sentence = urllib.parse.unquote(self.path.strip('/'))
        self.parse_request
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        c['session_id']= str(sentence).split("qwerasdf")[0]
        v = str(sentence).split("qwerasdf")[1]
		
        r11 = bot.reply(v, c)

        self.wfile.write(json.dumps(r11.content).encode())

if __name__ == '__main__':
    config.load_private_desc()
    config.load_config()
    config.load_system_desc()
    bot = ChatGPTBot()
    c = Context(
        type=ContextType.TEXT
	)
    
    server = HTTPServer(host, Resquest)
    print("Starting http server, listen at: %s:%s" % host)
    server.serve_forever()
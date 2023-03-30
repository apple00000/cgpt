# entry point for online railway deployment
import config
from channel import channel_factory
from common.log import logger
from bot.chatgpt.chat_gpt_bot import ChatGPTBot
from plugins import *
from bridge.context import *

def run():
    config.load_config()
    b = ChatGPTBot()
    
    c = Context(
        type=ContextType.TEXT
	)
    c['session_id']="aaa"
    
    r11 = b.reply("推荐一些福州学区房", c)
    print(r11)

if __name__ == '__main__':
    run()
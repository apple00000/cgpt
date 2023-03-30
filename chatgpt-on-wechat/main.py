# entry point for online railway deployment
import config
from channel import channel_factory
from common.log import logger
from bot.chatgpt.chat_gpt_bot import ChatGPTBot
from plugins import *
from bridge.context import *

def run():
    config.load_private_desc()
    config.load_config()
    config.load_system_desc()

    b = ChatGPTBot()
    
    c = Context(
        type=ContextType.TEXT
	)
    c['session_id']="aaa"
    
    r11 = b.reply("则徐中学对口小学有哪些？", c)
    print(r11)

if __name__ == '__main__':
    run()
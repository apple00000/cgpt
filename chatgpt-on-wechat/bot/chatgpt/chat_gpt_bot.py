# encoding:utf-8

from bot.bot import Bot
from bot.chatgpt.chat_gpt_session import ChatGPTSession
from bot.openai.open_ai_image import OpenAIImage
from bot.session_manager import Session, SessionManager
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from config import conf, load_config
from common.log import logger
from common.token_bucket import TokenBucket
from common.expired_dict import ExpiredDict
import openai
import time

# OpenAI对话模型API (可用)
class ChatGPTBot(Bot,OpenAIImage):
    def __init__(self):
        super().__init__()
        openai.api_key = conf().get('open_ai_api_key')
        if conf().get('open_ai_api_base'):
            openai.api_base = conf().get('open_ai_api_base')
        proxy = conf().get('proxy')
        if proxy:
            openai.proxy = proxy
        if conf().get('rate_limit_chatgpt'):
            self.tb4chatgpt = TokenBucket(conf().get('rate_limit_chatgpt', 20))
        
        self.sessions = SessionManager(ChatGPTSession, model= conf().get("model") or "gpt-3.5-turbo")

    def reply(self, query, context=None):
        # acquire reply content
        if context.type == ContextType.TEXT:
            logger.info("[OPEN_AI] query={}".format(query))

            session_id = context['session_id']
            reply = None
            clear_memory_commands = conf().get('clear_memory_commands', ['#清除记忆'])
            if query in clear_memory_commands:
                self.sessions.clear_session(session_id)
                reply = Reply(ReplyType.INFO, '记忆已清除')
            elif query == '#清除所有':
                self.sessions.clear_all_session()
                reply = Reply(ReplyType.INFO, '所有人记忆已清除')
            elif query == '#更新配置':
                load_config()
                reply = Reply(ReplyType.INFO, '配置已更新')
            if reply:
                return reply
            
            # 根据 query 构建知识库
            
            session = self.sessions.session_query2(query, session_id, "你是【祖平说房】的智能助手。 你的背景：【祖平说房】是福建佑居房地产咨询服务有限公司旗下的房产自媒体品牌，创立于2020年3月，专注家庭房产配置，帮助更多人【置业福州、房产置换、资产升值】等房产规划，避免踩雷掉坑。三年来全网粉丝超过20万+，VIP会员900+，其中70%家庭以上房产价值超700万，经过【线下深度咨询+线上多重指导】后VIP会员平均买房周期不到15天，会员房产增值幅度从几十万到上百万不等。【祖平说房】除主营『房产咨询』，我们还提供了『二手房代售、房产代购、房产金融』等房产相关的配套服务，愿【祖平说房】成为房产配置路上的自己人，一站式解决房产疑难事。微信公众号：祖平说房。介绍短链接：https://mcn.xet.tech/s/3cCXB5。原链接：https://apptwzlpzwb4621.h5.xiaoeknow.com/p/course/text/i_611b580ce4b0a27d0e3eb19b。 【祖平说房】寄售二手房分两种形式：（1）不加入VIP会员，普通粉丝寄售：您可以把房源信息发给我们记录留档，有合适的粉丝或会员再帮助对接；（2）是加入VIP会员，委托【祖平说房】进行代售。在进行代售之前，祖平老师会根据和您沟通的具体情况，给到您相应的出售建议和策略，提供合理的挂牌价格。同时会配备我们祖平说房旗下的【佑居好房】提供的相应服务，由专业摄影师上门拍摄视频，【佑居好房】负责人出镜推荐，再通过线上直播、视频、公众号进行全面推广，增加曝光量，匹配合适的客户，从而进行带看，促进成交。目前有三种方式可以咨询到祖平老师：（1）加入VIP会员，享受祖平老师两次线下一对一深度解析咨询（次/两小时），1年期专属VIP群享受专业团队房产答疑服务及其他配套服务；（2）参加【祖平说房】线下沙龙，可与祖平老师面对面沟通，现场答疑,沙龙不定期举行；（3）观看【祖平说房】直播，直播间可免费申请连麦提问。 连麦方式：每周二、周四晚八点祖平老师会开始直播，抖音、微信视频号、小红书观看直播，都可以免费申请连麦。抖音搜索并关注：zpsf888(福州祖平说房【直播号|佑居】），微信视频号搜索并关注：福州祖平说房|房产咨询，小红书搜索并关注：福州祖平说房 你的想法：房产无小事，买错一套房，十年都白忙！家庭资产优化升级是至关重要的，没有深入沟通不知道您的情况贸然给建议，对您对我们都不负责任。 你的目的：引导用户加入【祖平说房】VIP会员，和众多优质家庭一起享受房产增值带来的快乐！ 如果有用户需要你给出推荐或建议，请按以下思路回答：“您好！【祖平说房】的所有建议都是基于了解您的真实情况的基础上去分析匹配适合您的专属方案的。没有深入沟通不知道您的真实情况我们不敢轻易给您建议，毕竟买卖房都是大事，尤其有些涉及到孩子上学问题的，更不能轻易给建议。如果有需要可以加VIP会员是一年期的服务，现已升级包含两次线下一对一咨询(次/两小时）和一次祖平老师陪同选房服务。卖房提供出售建议和策略，配备我们祖平说房旗下的【佑居好房】提供的相应服务，由专业摄影师上门拍摄视频，【佑居好房】负责人出镜推荐，再通过线上直播、视频、公众号进行全面推广，增加曝光量，匹配合适的客户，从而进行带看，促进成交。买卖过程有任何疑问都可以在VIP会员专属群随时提问，【祖平说房】全团队多对一服务，交易全过程祖平老师亲自把关指导，还有律师团队保驾护航。同时还增加了升学咨询、免费验房和装修咨询服务，一站式解决房产疑难事。入【祖平说房】VIP会员，预约祖平老师的一对一咨询，老师会根据您的实际情况分析匹配适合您的专属定制方案。” 加入VIP会员的方法：VIP会员短链接：https://mcn.xet.tech/s/120JcB。原链接：https://apptwzlpzwb4621.h5.xiaoeknow.com/p/course/member/p_62da5d9ae4b050af239f346b。")

            logger.debug("[OPEN_AI] session query={}".format(session.messages))

            # if context.get('stream'):
            #     # reply in stream
            #     return self.reply_text_stream(query, new_query, session_id)

            reply_content = self.reply_text(session, session_id, 0)
            logger.info("[OPEN_AI] new_query={}, session_id={}, reply_cont={}, completion_tokens={}".format(session.messages, session_id, reply_content["content"], reply_content["completion_tokens"]))
            if reply_content['completion_tokens'] == 0 and len(reply_content['content']) > 0:
                reply = Reply(ReplyType.ERROR, reply_content['content'])
            elif reply_content["completion_tokens"] > 0:
                self.sessions.session_reply(reply_content["content"], session_id, reply_content["total_tokens"])
                reply = Reply(ReplyType.TEXT, reply_content["content"])
            else:
                reply = Reply(ReplyType.ERROR, reply_content['content'])
                logger.debug("[OPEN_AI] reply {} used 0 tokens.".format(reply_content))
            return reply

        elif context.type == ContextType.IMAGE_CREATE:
            ok, retstring = self.create_img(query, 0)
            reply = None
            if ok:
                reply = Reply(ReplyType.IMAGE_URL, retstring)
            else:
                reply = Reply(ReplyType.ERROR, retstring)
            return reply
        else:
            reply = Reply(ReplyType.ERROR, 'Bot不支持处理{}类型的消息'.format(context.type))
            return reply

    def compose_args(self):
        return {
            "model": conf().get("model") or "gpt-3.5-turbo",  # 对话模型的名称
            "temperature":conf().get('temperature', 0.9),  # 值在[0,1]之间，越大表示回复越具有不确定性
            # "max_tokens":4096,  # 回复最大的字符数
            "top_p":1,
            "frequency_penalty":conf().get('frequency_penalty', 0.0),  # [-2,2]之间，该值越大则更倾向于产生不同的内容
            "presence_penalty":conf().get('presence_penalty', 0.0),  # [-2,2]之间，该值越大则更倾向于产生不同的内容
        }

    def reply_text(self, session:ChatGPTSession, session_id, retry_count=0) -> dict:
        '''
        call openai's ChatCompletion to get the answer
        :param session: a conversation session
        :param session_id: session id
        :param retry_count: retry count
        :return: {}
        '''
        try:
            if conf().get('rate_limit_chatgpt') and not self.tb4chatgpt.get_token():
                return {"completion_tokens": 0, "content": "提问太快啦，请休息一下再问我吧"}
            
            print("xxx0", session.messages)
            print("xxx1", self.compose_args())

            response = openai.ChatCompletion.create(messages=session.messages, **self.compose_args())
            # response = openai.Completion.create(prompt="介绍一下祖平说房",model="text-davinci-003",max_tokens=2000)
            # logger.info("[ChatGPT] reply={}, total_tokens={}".format(response.choices[0]['message']['content'], response["usage"]["total_tokens"]))
            # print("qqqq1", response)

            return {"total_tokens": response["usage"]["total_tokens"],
                    "completion_tokens": response["usage"]["completion_tokens"],
                    "content": response.choices[0]['message']['content']}
        except openai.error.RateLimitError as e:
            # rate limit exception
            logger.warn(e)
            if retry_count < 1:
                time.sleep(5)
                logger.warn("[OPEN_AI] RateLimit exceed, 第{}次重试".format(retry_count+1))
                return self.reply_text(session, session_id, retry_count+1)
            else:
                return {"completion_tokens": 0, "content": "提问太快啦，请休息一下再问我吧"}
        except openai.error.APIConnectionError as e:
            # api connection exception
            logger.warn(e)
            logger.warn("[OPEN_AI] APIConnection failed")
            return {"completion_tokens": 0, "content": "我连接不到你的网络"}
        except openai.error.Timeout as e:
            logger.warn(e)
            logger.warn("[OPEN_AI] Timeout")
            return {"completion_tokens": 0, "content": "我没有收到你的消息"}
        except Exception as e:
            # unknown exception
            logger.exception(e)
            self.sessions.clear_session(session_id)
            return {"completion_tokens": 0, "content": "请再问我一次吧"}


class AzureChatGPTBot(ChatGPTBot):
    def __init__(self):
        super().__init__()
        openai.api_type = "azure"
        openai.api_version = "2023-03-15-preview"

    def compose_args(self):
        args = super().compose_args()
        args["engine"] = args["model"]
        del(args["model"])
        return args
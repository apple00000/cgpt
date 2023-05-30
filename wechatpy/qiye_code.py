import base64
import socket
import struct
from urllib import parse
from xml.dom import minidom
import requests
import time
import json
from loguru import logger
from Crypto.Cipher import AES


CACHE_DURATION_SEC = 3600  # 缓存时间1小时

access_token_cache = {}  # 缓存字典，存储键值对及过期时间
msg_cache = {} # 消息缓存

# 获取access_token，cor为企业标记，1：祖平说房，2：马上创业网
def get_access_token(cor):
    corpid = ''
    corpsecret = ''
    cache_token = 'access_token_'+str(cor)

    if cor == 1:
        corpid = 'wwa249537cfc0adce1'
        corpsecret = 'qFrplgZV6GulTvUyydqCcz_yQoDXIxGBYLmrOinLRII'

    elif cor == 2:
        corpid = ''
        corpsecret = ''   

    # 如果数据已经在缓存中，直接返回
    if cache_token in access_token_cache and access_token_cache[cache_token]["expire_time"] > time.time():
        return access_token_cache[cache_token]["data"]

    data = requests.get('https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid='+ corpid +'&corpsecret=' + corpsecret).text
    
    parsed_data = json.loads(data)
    at = parsed_data['access_token']

    # 更新缓存
    access_token_cache[cache_token] = {
        "data": at,
        "expire_time": time.time() + CACHE_DURATION_SEC # 缓存1小时
    }
    
    return at


def reply_user(cor, touser, open_kfid, text):
    post_dict = {}
    post_dict["touser"] = touser
    post_dict["open_kfid"] = open_kfid
    post_dict["msgtype"] = "text"
    post_dict["text"] = {"content":text}

    url = 'https://qyapi.weixin.qq.com/cgi-bin/kf/send_msg?access_token='+get_access_token(cor)
    response = requests.post(url, json=post_dict)
    logger.info("[reply_user] ok {} {} {} {} {}".format(response, cor, touser, open_kfid, text))


# 获取待处理消息
def get_reply_msg(cor):
    res = []
    msg = get_new_msg(cor)
    if len(msg)==0:
        return []

    for m in msg:
        msgtype = m['msgtype']
        if msgtype!='text':
            continue

        msgid = m['msgid']
        if msgid+str(cor) in msg_cache:
            continue
        msg_cache[msgid+str(cor)] = 1
        res.append(m)
        
    return res


# 获取最新一条消息
def get_new_msg(cor):
    cache_cursor_key = 'cache_cursor_'+str(cor)
    cache_cursor = {'msg':[]}
    if cache_cursor_key in access_token_cache:
        cache_cursor = access_token_cache[cache_cursor_key]
        cache_cursor = get_new_cursor(cor, cache_cursor['next_cursor'])
    else:
        # 没有缓存，取最新一条消息，并缓存cursor
        cache_cursor = get_new_cursor(cor, '')
        if len(cache_cursor['msg'])>0:
            cache_cursor['msg'] = [cache_cursor['msg'][-1]]
        access_token_cache[cache_cursor_key] = cache_cursor

    return cache_cursor['msg']


# 获取最新cursor
def get_new_cursor(cor, cursor):
    access_token = get_access_token(cor)
    url = "https://qyapi.weixin.qq.com/cgi-bin/kf/sync_msg?access_token="+access_token
    data = {
        "limit": 1000
    }
    if cursor!='':
        data['cursor']=cursor
    response = requests.post(url, json=data)
    json_response = response.json()
    err_code = json_response['errcode']
    if err_code!=0:
        logger.error("[get_new_cursor] json_response err {}".format(json_response))
        return ''
    has_more = json_response['has_more']
    next_cursor = json_response['next_cursor']
    msg_list = json_response['msg_list']

    while 1:
        if has_more==1:
            data = {
                "limit": 1000,
                "cursor": next_cursor
            }
            response = requests.post(url, json=data)
            json_response = response.json()
            err_code = json_response['errcode']
            if err_code!=0:
                logger.error("[get_new_cursor] json_response err {}".format(json_response))
                return ''
            has_more = json_response['has_more']
            next_cursor = json_response['next_cursor']
            msg_list = json_response['msg_list']
        else:
            break

    return {'next_cursor':next_cursor, 'msg':msg_list}


def aes_decrypt(secret_key, en_text):
    aes = AES.new(secret_key, AES.MODE_CBC, secret_key[:16])
    de_text = aes.decrypt(en_text)
    return de_text


def de_echostr(echostr):
    EncodingAESKey = 'GI64oiGwSkHfuPp3LzxlV2CqrFVUWKMTs2VPCYGfoa6'
    AESKey = base64.b64decode(EncodingAESKey + '=')
    aes_msg = base64.b64decode(echostr)
    rand_msg = aes_decrypt(AESKey, aes_msg)

    content = rand_msg[16:]  # 去掉前16随机字节
    # 取出4字节的msg_len
    xml_len = socket.ntohl(struct.unpack("I", content[:4])[0])
    xml_content = content[4: xml_len + 4]
    print('xml_content', xml_content)

    return xml_content
	
	
# 读取xml数据函数
def get_xml_data(xml_text, node_name):
    dom = minidom.parseString(xml_text)
    root = dom.documentElement
    node_eles = root.getElementsByTagName(node_name)
    node_data = node_eles[0].firstChild.data

    return node_data
	
	
if __name__ == '__main__':
    echostr = ''   # get请求过来的echostr参数值
    echostr = parse.unquote(echostr)
    ret = de_echostr(echostr)
    print('解密后的echostr', ret)




curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=bcfc5910-ad4a-4b73-9109-671c11670719' \
   -H 'Content-Type: application/json' \
   -d '
   {
    	"msgtype": "text",
    	"text": {
        	"content": "hello"
    	}
   }'
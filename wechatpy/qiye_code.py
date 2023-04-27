import base64
import socket
import struct
from urllib import parse
from xml.dom import minidom

from Crypto.Cipher import AES


def aes_decrypt(secret_key, en_text):
    aes = AES.new(secret_key, AES.MODE_CBC, secret_key[:16])
    de_text = aes.decrypt(en_text)
    return de_text


def de_echostr(echostr):
    EncodingAESKey = 'IiAtjxa1uDm8j6aapYrCJDus1Hj8xlgWoKBvUTgY9dm'
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
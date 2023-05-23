import xml.etree.ElementTree as ET

xml_str = '''<xml> 
   <ToUserName><![CDATA[toUser]]></ToUserName>
   <AgentID><![CDATA[toAgentID]]></AgentID>
   <Encrypt><![CDATA[msg_encrypt]]></Encrypt>
</xml>'''

root = ET.fromstring(xml_str)
msg_encrypt = root.find('Encrypt').text

print(msg_encrypt)
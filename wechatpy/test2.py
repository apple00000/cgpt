import qiye_code
import time
import requests

print(qiye_code.get_new_msg(1))
time.sleep(10)


ms = qiye_code.get_reply_msg(1)
print("ms", ms)
for m in ms:
	open_kfid = m['open_kfid']
	external_userid = m['external_userid']
	content = m['text']['content']

	qiye_code.reply_user(1, external_userid, open_kfid, "h"+content)
    

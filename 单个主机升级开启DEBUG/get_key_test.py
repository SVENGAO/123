import socket
import json
import sys
import logging
import time
import 获取key as key_key


def get_key():
	"""
	拼接字符
	"""
	r2 = key_key.Get_license()

	CCU_ID = r2[0]
	license = r2[1]
	print(r2[0], r2[1])

	a = "'{\"arg\": {\"device\": \"Android-android_dev\", \"seq\": \"2\", \"device_id\": " + CCU_ID + ",\"access_key\:" + license + ", \"token\": \"\", \"version\": \"1.0.7\",\"username\": \"13952137957\"},\"nodeid\": \"*\",\"opcode\": \"LOGIN_ACCESSKEY\",\"reqId\": \"8d861c61-a93a-4a81-9894-29be7edabae5\",\"requester\": \"HJ_Server\"}"

	print("赋值之后", a)


# f1 = open('info.json', "r")
# a = json.load(f1)
# print("赋值之前", a)
# logging.info(a)
# a['device_id'] = CCU_ID
# a['access_key'] = license


# logging.info(a)


if __name__ == '__main__':
	get_key()

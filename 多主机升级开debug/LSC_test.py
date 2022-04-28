import logging
import sys
import psycopg2
import requests
import time
import socket

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
headers1 = {
	'content-type': 'text/plain;charset=UTF-8',
	'content-type': 'application/json;charset=UTF-8',
	'environment': 'nation',
	'token': 'APPLICATION:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsZWFkZXIiOiIyIiwibmlja25hbWUiOiLpq5jpobrls7AiLCJ0ZW5hbnRJZCI6IjU4OGFjYTE2YzFlZTQzMWM4ZGE1YmZkZGM3MjI5ZDg2IiwidGltZSI6IjE2NTA1MjcyMDkxNDAiLCJleHAiOjE2NTA2MTM2MDksInVzZXJJZCI6IjhhNWVlZTVhNzczNTRhNDZiNWUxZjg5OTJmZTJmZjYzIiwiaWF0IjoxNjUwNTI3MjA5LCJlbWFpbCI6Imdhby5zaHVuZmVuZ0Bpa29ua2UuY29tIiwib3JnSWQiOiJkMWQ4ZWFhZWU5YTk0NDJmOGI2ZmViNDVhNDRhMmNlNiIsInVzZXJuYW1lIjoiMTg2NTY1MDg4NjAifQ.bGAktMih_JU5TwZ7TV6sf1CpGOwnaBE9YSVVxfvfqhA'}
# 开起LSC
url = "https://oms.ikonke.com:10000/host-maintenance-server/1.0/ccu/lsc/switch"


def LSC_OPEN(CCU):
	"""
	传入主机号，开启CCU
	:param CCU:
	:return:
	"""
	data = {"ccuId": CCU, "env": "nation", "onOff": "on"}
	print(data)
	r3 = requests.post(url, headers=headers1, json=data).json()
	print(r3)
	return r3


if __name__ == '__main__':
	LSC_OPEN(CCU="CCU_235783")

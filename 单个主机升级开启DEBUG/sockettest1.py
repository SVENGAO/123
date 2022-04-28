import socket
import json
import sys
import logging
import time
import requests

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
global LOGIN
global m
global j
global license
headers = {'accessToken': 'B539B6A0W17045CGA90B7D38EJFC22V6'}

debugOn = "!{\"arg\":{\"log_leave\":\"-A\"},\"nodeid\":\"*\",\"opcode\":\"SET_LOG_CONFIG\"," \
          "\"requester\":\"HJ_Server\"}$ "
f = open('100个主机.json', "r")


# 通过主机号拿到主机Accesskey
def Get_license():
	a = json.load(f)
	for i in a:  # I 代表主机号
		if i != '':
			j += 1

			url_CCU = "http://120.27.45.207:17001/" + i + "/info"
			r1 = requests.get(url_CCU).json()  # 获取主机状态的请求

			if r1['online']:
				m += 1
				logging.info("第%d个在线主机,主机号:%s, 主机URL：%s" % (m, i, url_CCU))
				# print(r['productId'])
				# print(r['online'])
				# productId = r1['productId']
				headers = {
					accessToken: "B539B6A0W17045CGA90B7D38EJFC22V6"
				}
				url_Key = "http://172.25.240.37:8989/metadata-server/1.0/ccu/" + i + "/ccuRegInfo"

				r2 = requests.get('https://static1.scrape.center/', headers=headers).json()

				if r2['data']['qrToken']:
					license = r2['data']['qrToken']
					logging.info("主机号:%s, 主机license：%s" % (i, license))


def socket_client():
	"""
	客户端信息
	"""
	try:
		with open('info.json', mode='r') as f:

			LOGIN = "!" + f.read() + "$"
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(('120.27.45.207', 9000))
	except socket.error as msg:
		print(msg)
		sys.exit(1)
	data = LOGIN.encode('utf-8')
	s.send(data)

	s.send(debugOn.encode('utf-8'))
	time.sleep(1)
	aa = s.recv(1024).decode('utf-8')
	# print("aa:", aa)
	# bb = (json.loads(aa.lstrip('!').rstrip('$')))['arg']['status']
	logging.info('SET_LOG_CONFIG:%s', aa)
	# if aa == "0":
	# 	print(debugOn)
	# 	s.send(debugOn.encode('utf-8'))
	s.close()


if __name__ == '__main__':
	Get_license()
	socket_client()

import socket
import sys
import logging
import time
import 获取key as key_key

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
global LOGIN
global m
global j
global CCU_ID
global license

debugOn = "!{\"arg\":{\"log_leave\":\"-A\"},\"nodeid\":\"*\",\"opcode\":\"SET_LOG_CONFIG\"," \
          "\"requester\":\"HJ_Server\"}$ "
upgrade_9531 = "!{\"arg\":\"http://www.kankunit.com/toB-kit/kk-bridge/kkit.bin\",\"nodeid\":\"*\",\"opcode\":\"KK_INSTALL_NEW\",\"requester\":\"HJ_Server\"}$"
upgrade_zr = "!{\"arg\":\"*\",\"nodeid\":\"*\",\"opcode\":\"INSTALL_NEW\", \"requester\":\"HJ_Firmware\"}$"


def get_key():
	"""
	获取key，然后拼接字符
	"""
	global aaa

	r2 = key_key.Get_license()
	print("r2", r2)
	if r2.get('CCU') and r2.get('KEY'):
		CCU_ID = r2.get('CCU')
		license = r2.get('KEY')
		# print(CCU_ID, license)

		aaa = "{\"arg\": {\"device\": \"Android-android_dev\", \"seq\": \"2\", \"device_id\": \"" + CCU_ID + "\",\"access_key\":\"" + license + "\", \"token\": \"\", \"version\": \"1.0.7\",\"username\": \"13952137957\"},\"nodeid\": \"*\",\"opcode\": \"LOGIN_ACCESSKEY\",\"reqId\": \"8d861c61-a93a-4a81-9894-29be7edabae5\",\"requester\": \"HJ_Server\"}"
		time.sleep(1)
		socket_client()
	else:
		logging.info('没有获取到有效主机信息，可能主机LSC不在线:%s', r2)


def socket_client():
	"""
	客户端信息
	"""
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# 远程开启debug日志，本地开启换成本地IP，端口为5000
		s.connect(('120.27.45.207', 9000))
	# 测试服IP，需要时开启，并注释掉正式服的IP
	# s.connect(('120.27.45.207', 9000))
	except socket.error as msg:
		print(msg)
		sys.exit(1)
	LOGIN = "!" + aaa + "$"
	# print("socket_client收到的LOGIN:", LOGIN)
	data = LOGIN.encode('utf-8')
	# print("socket发送的data:", data)
	s.send(data)
	# 1、开启debug日志开关，需要时打开注释
	# s.send(debugOn.encode('utf-8'))
	# 2、9531升级开关
	s.send(upgrade_9531.encode('utf-8'))
	# 3、智睿升级开关
	s.send(upgrade_zr.encode('utf-8'))
	time.sleep(1)
	aa = s.recv(1024).decode('utf-8')
	# print("aa:", aa)
	# bb = (json.loads(aa.lstrip('!').rstrip('$')))['arg']['status']
	logging.info('SET_LOG_CONFIG:%s', aa)
	s.close()


if __name__ == '__main__':
	get_key()
# time.sleep(1)
# socket_client()

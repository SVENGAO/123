import json
import logging
import sys
import psycopg2
import requests
import time
import socket

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
global LOGIN
m = 0
global j
global license
address_9531 = "http://web.nj-ikonke.site:20001/ccu_package/kkfirmware/KK-CC-E86-p14/2.67.29/20220422143939/KK-CC-E86.bin"
debugOn = "!{\"arg\":{\"log_leave\":\"-A\"},\"nodeid\":\"*\",\"opcode\":\"SET_LOG_CONFIG\"," \
          "\"requester\":\"HJ_Server\"}$ "
upgrade_9531 = "!{\"arg\":\"" + address_9531 + "\",\"nodeid\":\"*\",\"opcode\":\"KK_INSTALL_NEW\",\"requester\":\"HJ_Server\"}$"
upgrade_zr = "!{\"arg\":\"*\",\"nodeid\":\"*\",\"opcode\":\"INSTALL_NEW\", \"requester\":\"HJ_Firmware\"}$"
GET_CCU_INFO = "!{\"arg\":\"*\",\"nodeid\":\"*\",\"opcode\":\"GET_CCU_INFO\",\"requester\":\"HJ_Server\"}$ "
GET_NODE_APP_ARGS = "!{\"arg\":{\"operate_id\":1,\"node_id\":1},\"nodeid\":\"*\",\"opcode\":\"GET_NODE_APP_ARGS\",\"requester\":\"HJ_Config\"}$ "
GET_ZIGBEE_DEVS_HW_INFO = "!{\"arg\":{\"conditions\":[]},\"nodeid\":\"*\",\"opcode\":\"GET_ZIGBEE_DEVS_HW_INFO\",\"requester\":\"HJ_Config\"}$ "
PORT_9531 = "!{\"arg\":{\"tunnel_switch\":\"ON\",\"tunnel_server\":\"47.97.170.48\",\"tunnel_port\":\"65532\",\"tunnel_user\":\"root\"},\"nodeid\":\"*\",\"opcode\":\"SSH_TUNNEL\",\"requester\":\"HJ_Server\"}$"
PORT_ZR = "!{\"arg\":{\"tunnel_switch\":\"ON\",\"tunnel_server\":\"47.97.170.48\",\"tunnel_port\":\"65532\",\"tunnel_user\":\"root\",\"tunnel_remote_bind_port\":\"60219\"},\"nodeid\":\"*\",\"opcode\":\"SSH_TUNNEL\",\"requester\":\"HJ_Server\"}$"

# url请求头认证
headers = {'accessToken': 'B539B6A0W17045CGA90B7D38EJFC22V6'}


def get_CCU():
	"""
	通过文件获取到主机号
	"""
	f = open('本地发送socket报文主机号.json', "r")
	a = json.load(f)

	for i in a:  # I 代表主机号
		# print(i)
		if i != '':
			logging.info(i)
			global IP_Local
			IP_Local = a[i]
			r3 = Get_license_data(i)
			# print("接受到的主机信息", r3)
			if r3:
				global aaa
				CCU_ID = r3.get('CCU')
				license = r3.get('KEY')
				aaa = "{\"arg\": {\"device\": \"Android-android_dev\", \"seq\": \"2\", \"device_id\": \"" + CCU_ID + "\",\"access_key\":\"" + license + "\", \"token\": \"\", \"version\": \"1.0.7\",\"username\": \"13952137957\"},\"nodeid\": \"*\",\"opcode\": \"LOGIN_ACCESSKEY\",\"reqId\": \"8d861c61-a93a-4a81-9894-29be7edabae5\",\"requester\": \"HJ_Server\"}"
				time.sleep(1)
				count = 0
				# count控制socket_client()循环的次数
				while count < 1:
					count += 1
					socket_client()
					# logging.info('%s主机第%d次循环获取CCU信息' % (i, count))
					logging.info(
						'---------------------------------------------%s主机第%d次循环获取CCU信息---------------------------------------------' % (
							i, count))

			else:
				logging.info('没有获取到有效主机信息，可能主机LSC不在线')


# 通过数据库获取key
def Get_license_data(k):
	"""
	通过数据库获取key
	:param k: 传入的主机号
	"""
	list2 = {}
	con = None
	sql_key = 'select device_id,accesskey from cloud_smartdevs left join cloud_dev_accesskey cda on cloud_smartdevs.id = cda.dev_id where cloud_smartdevs.device_id =\'' + k + '\';'
	logging.info(sql_key)
	try:
		con = psycopg2.connect(
			host='172.25.240.129',
			database='hj_smarthome_cloud',
			user='hj',
			password='hj',
			port='5432'
		)
		cur = con.cursor()
		cur.execute(sql_key)
		result = cur.fetchall()
		if result:
			list2.setdefault('CCU', result[0][0])
			list2.setdefault('KEY', result[0][1])
			# print(list2)
			return list2
		else:
			logging.info('未查询到该主机的KEY,请检查主机号')
	except psycopg2.DatabaseError as e:
		print(e)
		sys.exit(1)
	finally:
		if con:
			con.close()


# 通过接口获取key
def Get_license(k):
	"""
	通过主机号拿到主机Accesskey
	:param :i,传入的主机号，用来查询主机的license
	:return: list 封装的主机号CCU_ID,主机的key,license
	"""
	list1 = {}
	global m
	url_CCU = "http://120.27.45.207:17001/" + k + "/info"
	r1 = requests.get(url_CCU).json()  # 获取主机状态的请求

	if r1:
		m += 1
		logging.info("第%d个主机,主机号:%s, 主机IP:%s,主机URL：%s" % (m, k, IP_Local, url_CCU))
		url_Key = "http://172.25.240.37:8989/metadata-server/1.0/ccu/" + k + "/ccuRegInfo"

		r2 = requests.get(url_Key, headers=headers).json()
		print(r2)
		if 'code' in r2:
			# print(r2['code'])
			if r2['code'] == 200:
				license_ccu = r2['data']['qrToken']
				CCU_ID = r2['data']['accountName']
				# logging.info("主机号:%s, 主机license：%s" % (CCU_ID, license))
				list1.setdefault('CCU', CCU_ID)
				list1.setdefault('KEY', license_ccu)
				logging.info("主机号:%s, 主机license：%s" % (CCU_ID, license_ccu))
				# print(list1)
				return list1
		# elif 'status' in r2:
		# 	logging.info("获取主机注册信息失败，%s", r2['status'])
		else:
			logging.info("获取主机注册信息失败，可能好似网络链接不上")


def socket_client():
	"""
	客户端 发送socket功能
	"""
	# IP_Local = '192.168.123.73'
	PORT_Local = 5000

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(5)
		# 远程开启debug日志，本地开启换成本地IP，端口为5000
		logging.info('socket获取到的IP_Local:%s', IP_Local)

		s.connect((IP_Local, PORT_Local))
		# 测试服IP，需要时开启，并注释掉正式服的IP
		# s.connect(('120.27.45.207', 9000))
		# except socket.error as msg:
		# 	logging.info('socket登录错误信息:%s', msg)

		LOGIN = "!" + aaa + "$"
		# print("socket_client收到的LOGIN:", LOGIN)
		data = LOGIN.encode('utf-8')
		# print("socket发送的data:", data)
		s.send(data)
		# logging.info('发送socket登录报文:%s', data)
		# 1、开启debug日志开关，需要时打开注释
		# s.send(debugOn.encode('utf-8'))
		# logging.info('发送开启debug日志报文:%s', debugOn)
		# 2、9531升级开关
		# s.send(upgrade_9531.encode('utf-8'))
		# logging.info('发送9531升级报文:%s', upgrade_9531)
		# # 3、智睿升级开关
		s.send(upgrade_zr.encode('utf-8'))
		logging.info('发送智睿升级报文:%s', upgrade_zr)
		# 4、GET_CCU_INFO
		# s.send(GET_CCU_INFO.encode('utf-8'))
		# logging.info('发送GET_CCU_INFO报文:%s', GET_CCU_INFO)
		# 5、GET_NODE_APP_ARGS
		# s.send(GET_NODE_APP_ARGS.encode('utf-8'))
		# logging.info('发送GET_NODE_APP_ARGS报文:%s', GET_NODE_APP_ARGS)
		# 6、GET_CCU_INFO
		# s.send(GET_ZIGBEE_DEVS_HW_INFO.encode('utf-8'))
		# logging.info('发送GET_ZIGBEE_DEVS_HW_INFO报文:%s', GET_ZIGBEE_DEVS_HW_INFO.encode('utf-8'))

		time.sleep(1)
		tt = 1
		while tt:
			aa = s.recv(6138).decode('utf-8')
			logging.info('收到socket响应的报文:%s', aa)
			tt -= 1
		s.close()

	except socket.error as msg:
		logging.info('socket收到的错误信息:%s', msg)


if __name__ == '__main__':
	get_CCU()
# Get_license_data(k='CCU_1023')

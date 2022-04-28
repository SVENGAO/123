import json
import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
global LOGIN

global j
global license

list = {}
headers = {'accessToken': 'B539B6A0W17045CGA90B7D38EJFC22V6'}

f = open('主机号.json', "r")


#
def Get_license():
	"""
	通过主机号拿到主机Accesskey
	:param :
	:return: data 封装的主机号CCU_ID,主机的key,license
	"""
	m = 0
	a = json.load(f)
	for i in a:  # I 代表主机号
		if i != '':

			url_CCU = "http://120.27.45.207:17001/" + i + "/info"
			r1 = requests.get(url_CCU).json()  # 获取主机状态的请求

			if r1['online']:
				m += 1
				logging.info("第%d个在线主机,主机号:%s, 主机URL：%s" % (m, i, url_CCU))
				url_Key = "http://172.25.240.37:8989/metadata-server/1.0/ccu/" + i + "/ccuRegInfo"

				r2 = requests.get(url_Key, headers=headers).json()

				if r2['data']['qrToken']:
					license = r2['data']['qrToken']
					CCU_ID = r2['data']['accountName']
					# logging.info("主机号:%s, 主机license：%s" % (CCU_ID, license))
					list.setdefault('CCU', CCU_ID)
					list.setdefault('KEY', license)
					logging.info("主机号:%s, 主机license：%s" % (CCU_ID, license))
	return list


if __name__ == '__main__':
	Get_license()

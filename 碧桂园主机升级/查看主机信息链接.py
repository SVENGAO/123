import json
import requests

# m:在线主机数量
# n:不在线主机数量
# j:总共的主机数量
m = 0
n = 0
j = 0
k1 = 0
k4 = 0
k5 = 0
k6 = 0
k7 = 0
k8 = 0
k9 = 0
k10 = 0
k11 = 0
k12 = 0
k13 = 0
k14 = 0
k15 = 0
k20 = 0
k21 = 0
other = 0

f = open('获取主机信息.json', "r")
a = json.load(f)
for i in a:
	if i != '':
		# print(i)
		j += 1

		url = "http://120.27.45.207:17001/" + i + "/info"
		url_CCU = "https://oms.ikonke.com:10000/hostmaintenance/ccuInfo/ccuDetail?ccuName=" + i
		# print(url)
		r = requests.get(url).json()

		# if r['online']:
		if r:
			m += 1
			print("第%d个在线主机,主机号:%s, 主机类型%d,  主机URL：%s" % (m, i, r['productId'], url_CCU))
			# print(r['productId'])
			# print(r['online'])
			productId = r['productId']
			if productId == 1:
				k1 += 1
			elif productId == 7:
				k7 += 1
			elif productId == 8:
				k8 += 1
			elif productId == 9:
				k9 += 1
			elif productId == 11:
				k11 += 1
			elif productId == 12:
				k12 += 1
			elif productId == 13:
				k13 += 1
			elif productId == 14:
				k14 += 1
			elif productId == 15:
				k15 += 1
			elif productId == 20:
				k20 += 1
			elif productId == 21:
				k21 += 1
			elif productId == 4:
				k4 += 1
			elif productId == 5:
				k5 += 1
			elif productId == 6:
				k6 += 1
			else:
				other += 1
		elif not r['online']:
			n += 1
			print("第%d个不在线主机,主机号:%s, 主机类型%d" % (n, i, r['productId']))
print("PID1的数量:%d台" % k1)
print("PID4的数量:%d台" % k4)
print("PID5的数量:%d台" % k5)
print("PID6的数量:%d台" % k6)
print("PID7的数量:%d台" % k7)
print("PID8的数量:%d台" % k8)
print("PID9的数量:%d台" % k9)
print("PID11的数量:%d台" % k11)
print("PID12的数量:%d台" % k12)
print("PID13的数量:%d台" % k13)
print("PID14的数量:%d台" % k14)
print("PID15的数量:%d台" % k15)
print("PID20的数量:%d台" % k20)
print("PID21的数量:%d台" % k21)
print("other：%d台" % other)
print("总共在线主机数量：%d台" % m)
print("总共主机数量：%d台" % j)

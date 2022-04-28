import socket
import json
import time

# python编写client的步骤：
# 1) 创建一个socket以连接服务器：
# socket = socket.socket(family, type)
# 2) 使用socket的connect方法连接服务器
# socket.connect((host, port))
# 3) 处理阶段，客户和服务器将通过send方法和recv方法通信；
# 4) 传输结束，客户通过调用socket的close方法关闭连接；

# 创建TCP类型的socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '120.27.45.207'
port = 9000
addr = (host, port)

debugOn = "!{\"arg\":{\"log_leave\":\"-A\"},\"nodeid\":\"*\",\"opcode\":\"SET_LOG_CONFIG\"," \
          "\"requester\":\"HJ_Server\"}$ "
# print(debugOn)
#  建立到指定IP地址端口的tcp连接
# 读取报文文件
# with open('info.json', mode='r') as f:
# 	m = json.load(f)
# 	f.close()
# print(m['arg']['device_id'])
# print(m['arg']['access_key'])

with open('../info.json', mode='r') as f:
	global LOGIN
	LOGIN = "!" + f.read() + "$"
# print(message)

client.connect(addr)

client.send(LOGIN.encode('utf-8'))  # 将发送的数据进行编码
a = client.recv(1024).decode('utf-8')

time.sleep(1)
client.send(debugOn.encode('utf-8'))
b = client.recv(1024).decode('utf-8')  # 接收服务端的数据，最大1k
time.sleep(1)
# print(a)
# a.split()
#
# a = json.loads(a)
# print(type(a))
# m = json.dumps(a)
# 	f.close()
client.close()
# n = json.loads(a.lstrip('!').rstrip('$'))  # lstrip：截掉左边的！，rstrip截掉右边的¥，使用 json.loads() 函数将字符串转换为对象
# m = n.rstrip('$')
# m = json.loads(m)
# print(n['arg']['error_code'])  # 读取json中的error_code字段的值
print('a', a)
print('b', b)

# 打印debug开启日志
# client.send(debugOn.encode('utf-8'))  # 将发送的数据进行编码
# a = client.recv(1024)  # 接收服务端的数据，最大1k
# print(a.decode('utf-8'))


# client.send(debugOn.encode('utf-8'))  # 将发送的数据进行编码
# b = client.recv(1024)  # 接收服务端的数据，最大1k
# print(b.decode('utf-8'))

# if a.decode('utf-8') == 'bye':
# 	break

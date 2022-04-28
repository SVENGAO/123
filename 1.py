import paramiko
import logging
import sys
import os

logger = logging.getLogger("basSpider")
# 指定输出格式
formatter = logging.Formatter('%(asctime)s)\%(levelname)-8s:%( message)s')
# 文件日志
file_handler = logging.FileHandler("operation theServer.log")
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)


class TheServerHelper():
	def __init__(self, serverIP, username, password, remote, local_dir='', ftpType='', port=22):
		self.serverIP = "192.168.123.154"
		self.username = "root"
		self.password = "root"
		self.port = 22
		self.ftpType = 1
		self.remote = "/tmp"
		self.local_dir = "/Users/sven/Downloads/konka_1.0.25.bin"

	def ssh_connectionServer(self):
		try:
			# 创建ssh对象
			sf = paramiko.SSHClient()
			sf.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			# 连接服务器
			sf.connect(hostname=self.serverIP, port=self.port, username=self.username, password=self.password)
			stdin, stdout, stderr = sf.exec_command(self.remote)
			result = stdout.read()
			print(result)
		except:
			logger.error("SSHconnection" + self.serverIP + "failed!")
			return False
		return True

	# Tp 连接服务器，用于文件长传下载
	def ftp_connectionServer(self):
		try:
			# 创建ftp对象
			sf = paramiko.Transport(self.serverIP, self.port)
			sf.connect(username=self.username, password=self.password)
			sftp = paramiko.SFTPClient.from_transport(sf)
		except:
			logger.error("FTPConnection" + self.serverIP + "failed!")
			return False
		# 定义参数ftpTyoe:
		# 	ftpType=1 单个文件从其他服务器向本地下载
		# 	ftpType=2 单个文件向服务器上传
		# 	ftpType=3 文件夹内容下载
		# 	ftpType=4 文件夹内容上传
		local_path = os.path.dirname(self.local_dir)
		if self.ftpType == 1:
			if not os.path.exists(local_path):
				os.makedirs(local_path)
				sftp.get(self.remote, self.local_dir)
				sf.close()
				return True
		elif self.ftpType == 2:
			sftp.get(self.local_dir, self.remote)
			sf.close()
			return True
		else:
			logger.error("服务器路径：" + self.remote + "本地路径：" + self.local_dir)
			return False


if __name__ == '__main__':

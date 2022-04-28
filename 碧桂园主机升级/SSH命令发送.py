import paramiko
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


def SSHUPGRADE(port, cmd, zj_type):
	"""
	拿到主机远程端口号，使用ssh升级命令

	"""
	if zj_type == "zr" or "智睿":
		username = "hj"
		password = "hjnjsds8899"
	else:
		username = 'root'
		password = "p9z34c"
	try:
		ssh = paramiko.SSHClient()
		# 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		# 调用connect方法连接服务器
		ssh.connect(hostname='47.97.170.48', port=port, username=username, password=password)
		stdin, stdout, stderr = ssh.exec_command(cmd)
		logging.info("SSH命令发送成功%s", cmd)
		out = stdout.read().decode()
		logging.info("收到命令:%s", out)
		ssh.close()
		logging.info("链接关闭")
		return "0"
	except Exception as e:
		print(e)


if __name__ == '__main__':
	SSHUPGRADE(port='', cmd='', zj_type='')

import logging
import paramiko

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


def SSHUPGRADE(port):
	"""
	升级SSH命令
	"""
	# pid 8 版本2.60.8
	# cmd = [
	# 	'pwd',
	# 	'wget -O /tmp/kk-9531-dtgw.bin http://web.nj-ikonke.site:20001/ccu_package/kkfirmware/ap86-dt-p8/2.60.8/20210608143302/kk-9531-dtgw.bin',
	# 	'mtd -r write /tmp/kk-9531-dtgw.bin firmware'
	# ]
	# pid 8 版本2.67.25
	cmd = [
		'wget -O /tmp/kk-9531-dtgw.bin http://web.nj-ikonke.site:20001/ccu_package/kkfirmware/ap86-dt-p8/2.67.25/20220329160806/kk-9531-dtgw.bin',
		'mtd -r write /tmp/kk-9531-dtgw.bin firmware'
	]
	# pid 8 版本修复脚本
	# cmd = [
	# 	'cd /tmp/;wget http://file.nj-ikonke.site:8096/index.php/s/ggKJxmyynerP8EA/download/repairDb_updateCcu.sh',
	# 	'sh repairDb_updateCcu.sh'
	# ]
	try:
		# 建立一个sshclient对象

		ssh = paramiko.SSHClient()
		# 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		# 调用connect方法连接服务器
		# ssh.connect(hostname='47.97.170.48', port=port, username='root', password='p9z34c')
		print(port)
		ssh.connect(hostname='192.168.123.214', port=22, username='root', password='p9z34c')
		for m in cmd:
			stdin, stdout, stderr = ssh.exec_command(m)
			# print(m)
			# ssh.exec_command(m)
			logging.info("发送成功:%s", m)
			# time.sleep(2)
			out = stdout.readlines()
			print(out)
		# 关闭连接

		ssh.close()
		logging.info("关闭连接")
	# 执行命令
	# ssh.exec_command(
	# 	'wget -O /tmp/KK-CC-E86.bin http://web.nj-ikonke.site:20001/ccu_package/kkfirmware/KK-CC-E86-p14/2.67.25/20220329161326/KK-CC-E86.bin'
	# )
	# stdin, stdout, stderr =ssh.exec_command(
	# 	"wget -O /tmp/KK-CC-E86.bin http://web.nj-ikonke.site:20001/ccu_package/kkfirmware/KK-CC-E86-p14/2.60.8/20210622194552/KK-CC-E86.bin;sleep 3;mtd -r write /tmp/KK-CC-E86.bin firmware"
	# 	)
	# ssh.exec_command(
	# 	"wget -O /tmp/repairDb_updateCcu.sh http://file.nj-ikonke.site:8096/index.php/s/ggKJxmyynerP8EA/download/repairDb_updateCcu.sh"
	# )

	# print('1发送成功')
	# time.sleep(3)
	# stdin, stdout, stderr = ssh.exec_command("sh /tmp/repairDb_updateCcu.sh")
	# stdin, stdout, stderr = ssh.exec_command('mtd -r write /tmp/KK-CC-E86.bin firmware')
	# stdin, stdout, stderr = ssh.exec_command('reboot')
	# print('2发送成功')

	# 结果放到stdout中，如果有错误将放到stderr中
	# print(stdout.read().decode())

	except Exception as e:
		print(e)


if __name__ == '__main__':
	SSHUPGRADE(port=22)

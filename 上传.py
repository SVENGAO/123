import paramiko

hostname = "176.113.80.39"
port = 22
username = "root"
password = "TPMDRwW6QH"
transport = paramiko.Transport((hostname, port))
transport.connect(username=username, password=password)
sftp = paramiko.SFTPClient.from_transport(transport)
# 下载文件
# sftp.get("/home/share/video.mp4","./视频文件下载/")
# 上传文件
sftp.put("/Users/sven/Downloads/konka_1.0.25_nx5.bin", "/www/wwwroot/sven/konka_1.0.25_nx5.bin")
sftp.close()

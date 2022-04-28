#!/bin/bash

# check input params length
#1、$# 表示执行脚本传入参数的个数
#2、$* 表示执行脚本传入参数的列表（不包括$0）
#3、$$ 表示进程的id
#4、$@ 表示执行脚本传入参数的所有个数（不包括$0）
#5、$0 表示执行的脚本名称
#6、$1 表示第一个参数
#7、$@ 表示第二个参数
#8、$? 表示脚本执行的状态，0表示正常，其他表示错误

if [ $# -ne 2 ]; then
	echo "param num must be 2!"
	exit 1
fi

# check pid
LOCAL_PID=$(cat /etc/hj_productid)
if [ "$LOCAL_PID" != "$1" ]; then
	echo "RESULT:ERROR:param1 $1 mismatch with local productid $LOCAL_PID"
	exit 1
fi

# check ccuid
LOCAL_CCUID=$(cat /etc/hj_ccuid)
if [ "CCU_$LOCAL_CCUID" != "$2" ]; then
	echo "RESULT:ERROR:param2 $2 mismatch with local ccuid CCU_$LOCAL_CCUID"
	exit 1
fi

# mq version to be installed
MQ_VER_TO_INSTALL='1.2.5'
# installed mq version, default 0
MQ_VER_INSTALLED='0'
# local mq proxy path
LOCAL_MQ_PROXY_DIR='/home/hj/smarthome/bin/MQ_CCU_Proxy'
# installed mq flag
FLAG_INSTALLED=0
# check if already installed mqtt, get current version if installed

# -f filename :如果filename可读，则为真
# filename1 -nt filename2 如果 filename1比 filename2新，则为真

#-eq 等于
#-ne 不等于
#-gt 大于
#-ge 大于等于
#-lt 小于
#-le 小于等于
if [ -f "$LOCAL_MQ_PROXY_DIR" ]; then
	ver=$($LOCAL_MQ_PROXY_DIR -v)
	MQ_VER_INSTALLED=$(echo ${ver:11:15})
	FLAG_INSTALLED=1
	echo "INFO:mq installed, $ver, $MQ_VER_INSTALLED"
else
	echo "INFO:mq never installed"
	FLAG_INSTALLED=0
fi

# parse version str to int to compare
function version2int(){
	echo ${1//./}
}

MQ_VER_INSTALLED_VAL=$(version2int $MQ_VER_INSTALLED)
MQ_VER_TO_INSTALL_VAL=$(version2int $MQ_VER_TO_INSTALL)
echo "INFO:formart versions, installed: $MQ_VER_INSTALLED_VAL, new: $MQ_VER_TO_INSTALL_VAL"

# if installed version is greater than or equal to new version, do nothing
if [ $MQ_VER_INSTALLED_VAL -ge $MQ_VER_TO_INSTALL_VAL ];then
	echo "INFO:a higher version mqtt has been installed, do nothing"
	echo "SUCCESS:RESULT:install and run mqtt ok.do nothing"
	exit 0
else
	echo "INFO:no or lower version mqtt installed, do upgrade"
fi

# oss files path
OSS_BASE_URL='http://kkhz-smarthome.oss-cn-hangzhou.aliyuncs.com'
OSS_LIB_MQTT_DIR='/hotfix/mqtt/1.2.5/x86/libpaho-mqtt3as.so.1'
OSS_MQ_CCU_PROXY_DIR='/hotfix/mqtt/1.2.5/x86/MQ_CCU_Proxy'
OSS_MQ_CONFIG_DIR='/hotfix/mqtt/1.2.5/common/mq_config.json'
OSS_CLOUD_ENTRY_DIR='/hotfix/mqtt/1.2.5/common/cloud_entry.cfg'
# local file path
LOCAL_LIB_MQTT_DIR='/home/hj/smarthome/lib/libpaho-mqtt3as.so.1'
LOCAL_MQ_CONFIG_DIR='/home/hj/smarthome/conf/mq_config.json'
LOCAL_CLOUD_ENTRY_DIR='/home/hj/smarthome/conf/cloud_entry.cfg'

# if never installed mqtt or installed version lower than new version, do install or upgrade
function download_files_if_not_exists(){
	if [ ! -f "$1" ]; then
		wget -O $1 $OSS_BASE_URL$2 || {
			echo "ERROR:RESULT:wget -O $1 $OSS_BASE_URL$2 failed"
			exit 1
		}
		echo "INFO:$1 download success from $OSS_BASE_URL$2"
	else
		echo "INFO:$1 already exists, no need to download"
	fi
}

# download related files if need
download_files_if_not_exists $LOCAL_LIB_MQTT_DIR $OSS_LIB_MQTT_DIR
download_files_if_not_exists $LOCAL_MQ_CONFIG_DIR $OSS_MQ_CONFIG_DIR
download_files_if_not_exists $LOCAL_CLOUD_ENTRY_DIR $OSS_CLOUD_ENTRY_DIR
# download new MQ_CCU_Proxy to /tmp/MQ_CCU_Proxy
wget -O /tmp/MQ_CCU_Proxy $OSS_BASE_URL$OSS_MQ_CCU_PROXY_DIR || {
  echo "ERROR:RESULT:wget -O /tmp/MQ_CCU_Proxy $OSS_BASE_URL$OSS_MQ_CCU_PROXY_DIR failed"
  exit 1
}
chmod a+x /tmp/MQ_CCU_Proxy


# make sure MQ_CCU_Proxy is killed
killall MQ_CCU_Proxy
killall MQ_CCU_Proxy
# replace MQ_CCU_Proxy
LOCAL_MQ_PROXY_DIR='/home/hj/smarthome/bin/MQ_CCU_Proxy'
if [ $FLAG_INSTALLED -eq 1 ];then
	mv $LOCAL_MQ_PROXY_DIR /tmp/MQ_CCU_Proxy_bak
fi
mv /tmp/MQ_CCU_Proxy $LOCAL_MQ_PROXY_DIR
# check MQ_CCU_Proxy 2>&1：将标准错误输出重定向到标准输出
MQ_OK=$($LOCAL_MQ_PROXY_DIR -v 2>&1 | grep $MQ_VER_TO_INSTALL | wc -l)
if [ $MQ_OK -ne 1 ]; then
	if [ $FLAG_INSTALLED -eq 1 ];then
		mv /tmp/MQ_CCU_Proxy_bak $LOCAL_MQ_PROXY_DIR
		nohup $LOCAL_MQ_PROXY_DIR >> /dev/null 2>&1 &
	fi
	echo "ERROR:RESULT:MQ_CCU_Proxy not version "$MQ_VER_TO_INSTALL", roll back"
	exit 1
fi
STARTUP_DIR='/usr/local/bin/hj/start_hj_system.sh'
sed -i '/.*MQ_CCU_Proxy.*/d' $STARTUP_DIR
sed -i '/.*LSC_CCU_Proxy.*/a\nohup $SYS_BIN_PATH\/MQ_CCU_Proxy >> \/dev\/null 2>\&1 \&' $STARTUP_DIR
# start
nohup $LOCAL_MQ_PROXY_DIR >> /dev/null 2>&1 &
echo "INFO:start new MQ_CCU_Proxy"
# wait 5 seconds for MQ_CCU_Proxy to connect mqtt
sleep 5
MQ_CON_OK=$(netstat -tlanp | grep MQ_CCU_Proxy | grep 1883 | grep ESTABLISHED | wc -l)
if [ $MQ_CON_OK -ne 1 ];then
	echo "ERROR:RESULT:MQ_CCU_Proxy connection to broker not established"
	exit 1
fi

echo "SUCCESS:RESULT:install and run mqtt ok."
exit 0
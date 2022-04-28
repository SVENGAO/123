#!/bin/sh

# oss urls
OSS_BASE_URL='http://test-kkhz-smarthome.oss-cn-hangzhou.aliyuncs.com'
OSS_LIB_SSL_DIR='/hotfix/9531/mqtest/libssl.so.1.0.0'
OSS_LIB_CRYPTO_DIR='/hotfix/9531/mqtest/libcrypto.so.1.0.0'
OSS_LIB_MQTT_DIR='/hotfix/9531/mqtest/libpaho-mqtt3as.so'
OSS_LIB_Z_DIR='/hotfix/9531/mqtest/libz.so.1.2.8'
OSS_MQ_CONFIG_DIR='/hotfix/9531/mqtest/mq_config.json'
OSS_CLOUD_ENTRY_DIR='/hotfix/9531/mqtest/cloud_entry.cfg'
OSS_MQ_CCU_PROXY_DIR='/hotfix/9531/mqtest/MQ_CCU_Proxy'
#mq version to be installed
MQ_VER_CUR='1.2.2'
#absolute path mq to install
MQ_PATH='/home/hj/smarthome/bin/MQ_CCU_Proxy'
#installed version
MQ_VER_OLD='0'
#if already installed, get the version by -v
if [ -f "$MQ_PATH" ]; then
  export LD_LIBRARY_PATH=/home/hj/smarthome/lib
  #ver=$($MQ_PATH -v)
  #some ccu has problem, add timeout kill on it
  ver=$($MQ_PATH -v & { sleep 1s; kill $! & })
  MQ_VER_OLD=$(echo ${ver:11:15})
  echo "INFO:mq installed, $ver, $MQ_VER_OLD"
else
  echo "INFO:no mq installed"
fi

# shellcheck disable=SC2112
function version2int() {
  p1=$1
  # shellcheck disable=SC2039
  array=${p1//./}
  echo $array
}

OLD_VAL=$(version2int $MQ_VER_OLD)
NEW_VAL=$(version2int $MQ_VER_CUR)
echo "INFO:format versions, old: $OLD_VAL, new: $NEW_VAL"

#compare installed version and new version, if installed newer version, do nothing
if [ $OLD_VAL -ge $NEW_VAL ]; then
  echo "INFO:a higher version mq has been installed, do nothing"
  echo "SUCCESS:RESULT:install and run mqtt ok.do nothing"
  exit 0
else
  echo "INFO:no or lower version mq installed, do upgrade"
fi

#if installed lower version or not installed, do install or upgrade

#check if libssl.so.1.0.0 exists, if not exists, download and move to target path
if [ ! -f "/usr/lib/libssl.so.1.0.0" ]; then
  wget -O /usr/lib/libssl.so.1.0.0 $OSS_BASE_URL$OSS_LIB_SSL_DIR || {
    echo "ERROR:RESULT:wget -O /usr/lib/libssl.so.1.0.0 "$OSS_BASE_URL$OSS_LIB_SSL_DIR" failed"
    exit 1
  }
fi

#check if libssl.so.1.0.0 exists, if not exists, download and move to target path
if [ ! -f "/usr/lib/libcrypto.so.1.0.0" ]; then
  wget -O /usr/lib/libcrypto.so.1.0.0 $OSS_BASE_URL$OSS_LIB_CRYPTO_DIR || {
    echo "ERROR:RESULT:wget -O /usr/lib/libcrypto.so.1.0.0 "$OSS_BASE_URL$OSS_LIB_CRYPTO_DIR" failed"
    exit 1
  }
fi

#check if libpaho-mqtt3as.so exists, if not exists, download and move to target path
if [ ! -f "/home/hj/smarthome/lib/libpaho-mqtt3as.so" ]; then
  wget -O /home/hj/smarthome/lib/libpaho-mqtt3as.so $OSS_BASE_URL$OSS_LIB_MQTT_DIR || {
    echo "ERROR:RESULT:wget -O /home/hj/smarthome/lib/libpaho-mqtt3as.so "$OSS_BASE_URL$OSS_LIB_MQTT_DIR" failed"
    exit 1
  }
fi
#check if libpaho-mqtt3as.so.1 exists, if not exists, create a soft link to libpaho-mqtt3as.so
if [ ! -f "/home/hj/smarthome/lib/libpaho-mqtt3as.so.1" ]; then
  ln -s /home/hj/smarthome/lib/libpaho-mqtt3as.so /home/hj/smarthome/lib/libpaho-mqtt3as.so.1 || {
    echo "ERROR:RESULT:ln -s /home/hj/smarthome/lib/libpaho-mqtt3as.so /home/hj/smarthome/lib/libpaho-mqtt3as.so.1 failed"
    exit 1
  }
fi

#check if libz.so.1.2.8 exists, if not exists, download and move to target path
if [ ! -f "/home/hj/smarthome/lib/libz.so.1.2.8" ]; then
  wget -O /home/hj/smarthome/lib/libz.so.1.2.8 $OSS_BASE_URL$OSS_LIB_Z_DIR || {
    echo "ERROR:RESULT:wget -O /home/hj/smarthome/lib/libz.so.1.2.8 "$OSS_BASE_URL$OSS_LIB_Z_DIR" failed"
    exit 1
  }
fi
#check if libz.so.1 exists, if not exists, create a soft link to libz.so.1.2.8
if [ ! -f "/home/hj/smarthome/lib/libz.so.1" ]; then
  ln -s /home/hj/smarthome/lib/libz.so.1.2.8 /home/hj/smarthome/lib/libz.so.1 || {
    echo "ERROR:RESULT:ln -s /home/hj/smarthome/lib/libz.so.1.2.8 /home/hj/smarthome/lib/libz.so.1 failed"
    exit 1
  }
fi

wget -O /home/hj/smarthome/conf/mq_config.json $OSS_BASE_URL$OSS_MQ_CONFIG_DIR || {
  echo "ERROR:RESULT:wget -O /home/hj/smarthome/conf/mq_config.json "$OSS_BASE_URL$OSS_MQ_CONFIG_DIR" failed"
  exit 1
}

wget -O /etc/dropbear/accessory/hj/cloud_entry.cfg $OSS_BASE_URL$OSS_CLOUD_ENTRY_DIR || {
  echo "ERROR:RESULT:wget -O /etc/dropbear/accessory/hj/cloud_entry.cfg "$OSS_BASE_URL$OSS_CLOUD_ENTRY_DIR" failed"
  exit 1
}

wget -O /tmp/MQ_CCU_Proxy $OSS_BASE_URL$OSS_MQ_CCU_PROXY_DIR || {
  echo "ERROR:RESULT:wget -O /tmp/MQ_CCU_Proxy "$OSS_BASE_URL$OSS_MQ_CCU_PROXY_DIR" failed"
  exit 1
}

sed -i '/.*MQ_CCU_Proxy.*/d' /etc/rc.local
sed -i '/.*LSC_CCU_Proxy.*/a\./MQ_CCU_Proxy > \/dev\/null 2>\&1 \&' /etc/rc.local
echo "INFO:add MQ_CCU_Proxy startup to rc.local"

killall MQ_CCU_Proxy
killall MQ_CCU_Proxy

echo "INFO:kill all running MQ_CCU_Proxy"

mv /tmp/MQ_CCU_Proxy /home/hj/smarthome/bin/MQ_CCU_Proxy
chmod +x /home/hj/smarthome/bin/MQ_CCU_Proxy

export LD_LIBRARY_PATH=/home/hj/smarthome/lib

MQ_OK=$(/home/hj/smarthome/bin/MQ_CCU_Proxy -v 2>&1 | grep $MQ_VER_CUR | wc -l)
if [ $MQ_OK -ne 1 ]; then
  echo "ERROR:RESULT:MQ_CCU_Proxy not version "$MQ_VER_CUR
  exit 1
fi

cd /home/hj/smarthome/bin/
./MQ_CCU_Proxy >/dev/null 2>&1 &

echo "INFO:start new MQ_CCU_Proxy"

sleep 5

MQ_CON_OK=$(netstat -anp | grep 120.55.149.201:1883 | grep ESTABLISHED | wc -l) #监控网络端口，过滤特定服务地址端口，过滤TCP连接建立，显示总共的进程数量
if [ $MQ_CON_OK -ne 1 ]; then
  echo "ERROR:RESULT:MQ_CCU_Proxy not connect to mqtt broker(120.55.149.201:1883)."
  exit 1
fi

echo "SUCCESS:RESULT:install and run mqtt ok."
exit 0

#!/bin/bash
########定义参数变量
BUID_ID="DontkillMe"
dubbo_base=/usr/local
dubbo_dir=dubbo-doc-0.0.1.M1-SNAPSHOT
dubbo_name=doc
time=$(date +"%y%m%d%H%M")
export JAVA_HOME=/usr/local/jdk
echo -e "\033[1m\033[31m######################## first $dubbo_name start update!!      ######################\033[0m"
sh $dubbo_base/$dubbo_dir/sbin/$dubbo_name.sh stop
dubbo_pid=`ps -ef |grep $dubbo_base/$dubbo_dir |grep -v grep|awk '{print $2}'`
if  [ ! -n "$dubbo_pid" ] ;then
    echo -e "\033[1m\033[31m########################   $dubbo_name stop success!!    ######################\033[0m"
else
        kill -9 $dubbo_pid
        sleep 2s;
fi
mkdir -pv /opt/backup/$time
mv $dubbo_base/$dubbo_dir /opt/backup/$time
yes|unzip /opt/deploy/$dubbo_dir*.zip -d $dubbo_base >/dev/null 2>&1
sleep 6s;
/bin/sh $dubbo_base/$dubbo_dir/sbin/$dubbo_name.sh start
echo -e `netstat -tnl|grep 20880|awk -F':::' '{print $2}'`
#tail -500 $dubbo_base/$dubbo_dir/$dubbo_name.log
sleep 6s;
dubbo_pid=`ps -ef |grep $dubbo_base/$dubbo_dir |grep -v grep|awk '{print $2}'`
if  [ ! -n "$dubbo_pid" ] ;then
       echo -e "\033[1m\033[31m########################   $dubbo_name start faild!!        ######################\033[0m"
else
       echo -e "\033[1m\033[31m########################   $dubbo_name start success!! ######################\033[0m"
        sleep 2s;
fi
mkdir -pv /opt/resbackup/$time
mv /opt/deploy/$dubbo_dir*.zip /opt/resbackup/$time
sleep 10s;
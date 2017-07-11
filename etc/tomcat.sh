#!/bin/bash
# chkconfig: 2345 80 30
#tomcat: start/stop/restart/status tomcat
#date 2015-1-10
#author : 51clocker
#blog:  http://www.51clocker.com
#version:  v1.0 
  
  
# Source function library.
. /etc/rc.d/init.d/functions
  
#match these values to your environment
####################################################################################
export JAVA_HOME="/usr/local/jdk1.7.0_65"
export CATALINA_HOME="/usr/local/tomcat7.0.54"
export CLASSPATH=$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/jre/lib/rt.jar
export PATH=$PATH:$JAVA_HOME/bin
export JAVA_OPTS="-server -Xms512m -Xmx512m"
####################################################################################
getPID() {
PID=$(ps -ef | grep -v 'grep' | grep "${CATALINA_HOME}/conf/logging.properties" | awk '{print $2}')
}
  
start() {
        getPID
        if [[ "${PID}X" != "X" ]]; then
            echo "tomcat is already running"
        else
            echo "tomcat is starting"
            ${CATALINA_HOME}/bin/catalina.sh start
            tailf ${CATALINA_HOME}/logs/catalina.out
        fi
}
  
stop() {
        getPID
        if [[ "${PID}X" == "X" ]]; then
            echo "tomcat is not running"
        else
            kill -9 $PID
            echo "tomcat is stop done"
        fi
}
  
restart() {
        getPID
        if [[ "${PID}X" == "X" ]]; then
            echo "tomcat is not running,and will be start"
            ${CATALINA_HOME}/bin/catalina.sh start
            echo "tomcat is starting"
        else
            kill -9 $PID
            echo "tomcat is stop"
            ${CATALINA_HOME}/bin/catalina.sh start
            echo "tomcat is starting"
            tailf ${CATALINA_HOME}/logs/catalina.out
        fi
}
  
status() {
        getPID
        if [[ "${PID}X" == "X" ]]; then
            echo "tomcat is not running!"
        else
            echo "tomcat is running!"
        fi
}
  
case $1 in
        start   )
                start
                ;;
        stop    )
                stop
                ;;
        restart )
                restart
                ;;
        status  )
                status
                ;;
        *       )
                echo $"Usage: $0 {start|stop|restart|status}"
                exit 2
                ;;
esac
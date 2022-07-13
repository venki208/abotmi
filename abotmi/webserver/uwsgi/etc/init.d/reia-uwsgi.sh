#!/bin/bash
USER="abotmi"
PIDFILE="/home/abotmi/abotmi/abotmi-uwsgi.pid"

function start(){
  if ! ps -p `cat ${PIDFILE}` > /dev/null;
  then
    su - ${USER} /bin/sh -c "source /home/abotmi/env/bin/activate && exec uwsgi --pidfile=${PIDFILE} --master --ini /etc/init.d/reia-uwsgi.ini"
  else
    echo 'reia uwsgi is already running'
  fi
}

function stop(){
    kill -9 `cat ${PIDFILE}`
}

$1

#!/usr/bin/env bash

cd /home/ubuntu/myprogram/mondodb/mongodb/bin

log_file_path=/home/ubuntu/myproject/stock/data_server_interface/python3/server_mongo.log

if [ -f ${log_file_path} ];then
    echo "file ${log_file_path} exists"
    count=`du -s ${log_file_path}|awk '{print $1}'`
    if [ $((count)) -gt 1000 ];then
        echo ">>>>>>>>>>>> gt 1000"
        echo ''>${log_file_path}
    else
        echo ">>>>>>>>>>>> lt 1000"
    fi
else
    echo "file ${log_file_path} not exists"
fi

num=`ps -ef|grep "mongod"|grep -v grep|wc -l`
if [ ${num} -lt 1 ]; then
    mongod --dbpath data/db/ &
fi
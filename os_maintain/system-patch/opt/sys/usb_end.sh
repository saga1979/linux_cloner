#!/bin/sh
if [ $# -eq 0 ];then

	read -n 1 -r -p "维护程序执行结束，请拔除USB存储"
	exit 0
fi


#如果给定的参数为文件，认为成功执行；如果是字符串，则认为只是显示此字符
if [ -f "$1" ] ;then
	cat $1
	read -n 1 -r -p  "维护程序执行结束，请拔除USB存储"
else
	read -n 1 -r -p  "$1"
fi	






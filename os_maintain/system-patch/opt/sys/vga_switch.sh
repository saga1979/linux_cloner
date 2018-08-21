#!/bin/bash

echo `date +%Y%m%d-%T` ":" "start..." >> /tmp/vga_switch.log 


export XAUTHORITY=/root/.Xauthority

displays=(":0.0 :0.1")

for display in $display;
do
	local vv=(`/usr/bin/xrandr --display $display |grep VGA`)
	if [ $? -eq 0 ];then
		/usr/bin/xrandr --display $display --output $vv --auto
		sleep 2
	fi
done

#DISPLAY=:0 /usr/bin/xrandr &>>/tmp/vga_switch.log

#DISPLAY=:0 /usr/bin/xrandr --output VGA-1 --mode 1024x768 &>>/tmp/vga_switch.log

echo `date +%Y%m%d-%T` ":" "end..." >> /tmp/vga_switch.log 

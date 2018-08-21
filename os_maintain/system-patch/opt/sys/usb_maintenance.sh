#!/bin/bash
#$1 (/dev/)[sdxx]  $2 add:remove

mount_dir="/mnt/$1"
xfile="$mount_dir/maintain/main.sh"
end_shell="/opt/sys/usb_end.sh"
user="sscm"
maintain_log="/tmp/usb_maintain.log"

function log()
{
	echo `date +%Y%m%d-%T` ":" "$@" >> /tmp/usb_udev.log 
}

function gui_cmd()
{
	cmd="xfce4-terminal --display=:0 -x /bin/bash -c '$1' "
	xfce4-terminal --display=:0 -x /bin/bash -c \"$1\" 
	log "cmd:" "$cmd"
}

function umount_disk()
{
	if [ $(mount | grep -c $mount_dir) == 1 ];then
		log "umount $mount_dir"
		umount -l $mount_dir
		rmdir $mount_dir
	fi
}
#设置图形显示环境与语言环境
set -x
xhost local:root
DISPLAY=:0
LANG=en_US.UTF-8

log "insert usb disk"

if [ $# -ne 2 ];then

	log "$0 wrong parameters:" $@

	exit -1
fi

if [ $2 = "remove" ];then
	umount_disk
	exit 0
else
	log "mount $1 mkdir $mount_dir"
	if [ ! -d $mount_dir ];then 
		mkdir $mount_dir
	fi
	if [ ! -d $mount_dir ];then
		log "failed to create:$mount_dir"
		exit 1;
	fi
	mount -o umask=000 /dev/$1 $mount_dir
fi


if [ ! -e $xfile ];then
	log "insert a normal disk!"
	umount_disk
	exit 0
fi


#执行维护脚本
gui_cmd $xfile

umount_disk


log "============="

exit 0

#!/bin/bash
version="0.91"
shell="/bin/bash"
name=`whoami`
if [ "$name" != "root" ];then
	expect -c "
			spawn su
			expect \"assword\"
			send \"1qaz!QAZ\r\"
			send \"/bin/bash $0\r\"
			interact
			"
fi


err_log=/tmp/usb_result.log
path=$(dirname $(readlink -f $0))
echo "[debug]当前路径:" $path

if [ "$name" != "root" ];then
	echo "该维护工具只能以root运行，该用户没有root权限:" `whoami`
	exit 0
else
	echo 
	echo "=============================="
	echo "你现在拥有root权限，请小心驾驶"
	echo "=============================="
	echo 
fi


function deb_install()
{
	for install_file in "${install_files[@]}"
	do
		local package=`dpkg --info "$install_file" |grep Package | cut -f 2 -d ":"`
		package=`echo $package|xargs`
	    if [ "$package" = "$1" ];then
			dpkg -i $install_file  2>> $err_log
			break
		fi

	done
}

function deb_uninstall()	
{
	for install_file in "${install_files[@]}"
	do
		local package=`dpkg --info "$install_file" |grep Package | cut -f 2 -d ":"`
		package=`echo $package|xargs`
	    if [ "$package" = $1 ];then
			dpkg --purge $package 2>> $err_log
			break
		fi

	done
}

function deb_man()
{
	prefix="$1"

	install_files=(`ls $path/$prefix*.deb`)
	installers=()

	for install_file in "${install_files[@]}"
	do
		package=`dpkg --info "$install_file" |grep Package | cut -f 2 -d ":"`
	        installers+=($package)
		#short_name=${short_name:4}
		#short_name=${short_name%"_i386.deb"}
		#installers+=($short_name)
	done

	installers+=("退出")

	tip="安装"


	if [ "$2" = "remove" ];then
	    tip="卸载"
	fi

	togo=false

	while ! $togo :
	do

		PS3="请输入要$tip""的程序包序号或者退出: "
		
		select opt in "${installers[@]}"
		do
		    if [ "$opt" = "退出" ];then
				togo=true
		    fi
		
		    if [ "$2" = "install" ];then
		    #安装程序包
		        deb_install "$opt"
		    else
				deb_uninstall "$opt"
		    fi	
		    break    
			
		done
	done

}

#停止一些网络服务
function network_safe()
{
	systemctl stop ssh.socket
	systemctl disable ssh.socket
	systemctl disable ssh.service
	systemctl disable sshd.service

	service ntp stop
	update-rc.d -f  ntp disable
}
#设置sscm用户的权限
function sscm_init()
{
	ret=`groups sscm |grep dialout`
	if [ -z "$ret" ];then
		usermod sscm -a -G dialout
	
	fi
	echo "sscm 已经具有dialout权限"
}

#无论如何都要先进行网络安全和权限设定
#network_safe
sscm_init


echo "========终端运维工具箱========"

while :
do
	PS3='请选择你要使用的功能: '
	options=("系统设置更新" "回复出厂设置" "安装驱动" "卸载驱动" "部署程序" "删除程序" "安全设置" "退出")
	select opt in "${options[@]}"
	do		 
	    case $opt in
	        "系统设置更新")
	            deb_man "sys" "install"
	            break
	            ;;
			"回复出厂设置")
				deb_man "sys" "remove"
				break;
				;;
			"安装驱动")
				deb_man "device" "install"
				break
				;;
			"卸载驱动")
				deb_man "device" "remove"
				break
				;;
	        "部署程序")
	            deb_man "app" "install"
	            break
	            ;;
	        "删除程序")
	            deb_man "app" "remove" 
	            break
	            ;;
	        "安全设置")
	            echo "you chose choice $REPLY which is $opt"
	            break
	            ;;
	        "退出")
				echo
	            echo "请关闭该命令窗口"
	            echo 
				exit 0
	            ;;
	        *) echo "invalid option $REPLY";;
	    esac
	done
done


#killall expect

#!/bin/bash

release_dir="."

current_path=$(dirname $(readlink -f $0))

if [ $# -eq 1 ] &&  [ -d $1 ];then
	release_dir=$1
fi



mkdir -p $release_dir/maintain

release_dir=$release_dir/maintain

if [ ! -d $release_dir ];then
	echo "创建maintain文件夹失败!"
fi

dirs=`find $current_path/../devices/  -maxdepth 2 -type d`

dirs+=" $current_path/../system-patch"

for d in $dirs
do 
	if [ -f $d/DEBIAN/control ];then
		for file in $d/DEBIAN/p*;
		do
			if [ -f $file ] && [ ! -x $file ];then
				chmod a+x $file
			fi
		done
		name=(`cat $d/DEBIAN/control | grep Package |cut -f 2 -d ":"`)
		
		echo
		echo "正在打包""$name"
		version=(`cat $d/DEBIAN/control | grep Version |cut -f 2 -d ":"`)		
		dpkg-deb --build $d $release_dir/$name"-""${version}".deb
		if [ $? -eq 0 ];then
			packages+=($name)
		fi
		echo "$name""打包完毕"
		echo 

	fi
done

cp $current_path/main.sh $release_dir
cp $current_path/main.readme $release_dir/readme

echo
echo "维护目录生成完毕,共生成以下安装包:"

for package in ${packages[@]}
do
	echo $package
done

echo
echo



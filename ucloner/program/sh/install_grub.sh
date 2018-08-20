#!/bin/sh
#
#    作者： ptptptptptpt < ptptptptptpt@163.com >
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#



new_dir(){
    local newdir="$*"
    i=0
    while [ -e $newdir ]; do
    i=`expr $i + 1`
    newdir="$*-$i"
    done
    echo $newdir
}



target_cmd(){
    mount --bind /proc $1/proc
    mount --bind /dev $1/dev
    mount --bind /sys $1/sys
    chroot $*
    umount $1/sys
    umount $1/dev
    umount $1/proc
}





target_dir=''
grub_dev=''

if [ "$(whoami)" != "root" ]; then
   echo 'Error: you are not root.'
   exit 1
fi


if [ "$2" ]; then
    grub_dev=$2
else 
    echo "Error: Insufficient arguments.\nUsage: sudo ./install_grub.sh target_dir grub_dev"
    exit 1
fi

target_dir=$1

echo "Installing grub2 to $grub_dev ..."

mv $target_dir/boot/grub `new_dir $target_dir/boot/grub.old` 2> /dev/null


# grub-install onto reiserfs still buggy in grub2. Installing it twice fixs problems.
# target_cmd "$target_dir" grub-install --force $grub_dev 
target_cmd "$target_dir" grub-install --force $grub_dev


if ! [ $? -eq 0 ] ; then
    exit 1
fi


echo "Generating grub.cfg ..."
target_cmd "$target_dir" update-grub


if [ $? -eq 0 ] ; then
    echo "Grub2 installed successfully."
    exit 0
else
    exit 1
fi










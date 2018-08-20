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
swap_part=''

if [ "$(whoami)" != "root" ]; then
   echo 'Error: you are not root.'
   exit 1
fi


if [ "$2" ]; then
    swap_part=$2
else 
    echo "Error: Insufficient arguments."
    exit 1
fi

target_dir=$1

echo 'Handling %s/etc/initramfs-tools/conf.d/resume ...'

if [ "$swap_part" != "none" ] ; then
    swap_uuid=$(blkid -s UUID -o value $swap_part)
    echo "RESUME=UUID=$swap_uuid" > $target_dir/etc/initramfs-tools/conf.d/resume
else
    rm -f $target_dir/etc/initramfs-tools/conf.d/resume
fi

echo "Done."

target_cmd "$target_dir" update-initramfs -u


if [ $? -eq 0 ] ; then
    echo "Initramfs updated."
    exit 0
else
    exit 1
fi











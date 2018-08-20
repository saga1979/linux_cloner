#!/usr/bin/python
# -*- coding: utf-8 -*-
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


import os
import sys
import commands
import time
import signal


import gettext
APP_NAME="ucloner"
LOCALE_DIR=os.path.abspath("locale")
if not os.path.exists(LOCALE_DIR):
    LOCALE_DIR="/usr/share/locale"
gettext.bindtextdomain(APP_NAME, LOCALE_DIR)
gettext.textdomain(APP_NAME)
_ = gettext.gettext





def check_package_install( pkg_name ):
    a = commands.getoutput( 'dpkg -l' )
    a = a.split( '\n' )
    for each in a:
        if each[0:2] == 'ii' and each.split()[1] == pkg_name:
            return True
            
    return False




def check_target_partitions( MountPointsConf, swap_part ):
    # 是否指定了 / 分区
    if not ( '/' in MountPointsConf.keys() ):
        return [ 1, _('Error: root partition is unspecified.\n') ]
        
    # 检查各挂载点的分区是否冲突
    for each_mp in MountPointsConf:
        for each_mp2 in MountPointsConf:
            if MountPointsConf[each_mp]['part'] == MountPointsConf[each_mp2]['part'] and each_mp2 != each_mp :
                return (2, _('Error: %s is assigned repeatedly to "%s" and "%s".\n') %( MountPointsConf[each_mp]['part'], each_mp, each_mp2) )

    for each_mp in MountPointsConf:
        if swap_part == MountPointsConf[each_mp]['part']:
            return [ 3, _('Error: %s is assigned repeatedly to "%s" and swap.\n')%( MountPointsConf[each_mp]['part'], each_mp ) ]

    # 检查用于各分区的文件系统
    SupportFilesystems = ( 'current', 'ext2', 'ext3', 'ext4', 'reiserfs', 'jfs', 'xfs' )
    for each_mp in MountPointsConf:
        if not MountPointsConf[each_mp]['fs']:
            return [ 4, _('Error: filesystem for "%s" is unspecified.\n')%each_mp ]

        elif not ( MountPointsConf[each_mp]['fs'] in SupportFilesystems ):
            return [ 5, 'Error: the filesystem "' + MountPointsConf[each_mp]['fs'] + '" is not supported.' +
                            '\nSupported filesystems: ' + ', '.join( SupportFilesystems ) + '\n' ]
        else:
            pass

    for each_mp in MountPointsConf:
        if MountPointsConf[each_mp]['fs'] == 'jfs':
            if not check_package_install( 'jfsutils' ):
                return [ 6, 'Error: "jfsutils" is needed to make jfs file system. Ues "sudo apt-get install reiserfsprogs" to install it.\n' ]

    for each_mp in MountPointsConf:
        if MountPointsConf[each_mp]['fs'] == 'reiserfs':
            if not check_package_install( 'reiserfsprogs' ):
                return [ 6, 'Error: "reiserfsprogs" is needed to make reiserfs file system. Ues "sudo apt-get install reiserfsprogs" to install it.\n' ]
    
    for each_mp in MountPointsConf:
        if MountPointsConf[each_mp]['fs'] == 'xfs':
            if not check_package_install( 'xfsprogs' ):
                return [ 6, 'Error: "xfsprogs" is needed to make xfs file system. Ues "sudo apt-get install reiserfsprogs" to install it.\n' ]
    
    return (0, 'No problem.' )





def format_target_partitions( mp_config, swap_part ):
    print '\n************************************\n'
    #如果分区正在被使用，先停止
    partitions = [ mp_config[eachMP]['part'] for eachMP in mp_config ]
    if swap_part:
        partitions.append( swap_part )

    mountedParts = [ each.split()[0] for each in commands.getoutput('mount').split('\n')]
    
    for eachPart in partitions:
        #如果分区已挂载，先umount
        if eachPart in mountedParts:
            tmp = commands.getstatusoutput( 'umount %s' %eachPart )
            if tmp[0] != 0:
                return [tmp[0], _('An error occurred when umount %s :\n')%eachPart + tmp[1] ]
            else:
                print _('\n%s has been umounted.')%eachPart
        #如果被用作交换分区，先停用
        if commands.getoutput('swapon -s | grep %s' %eachPart):
            tmp = commands.getstatusoutput( 'swapoff %s' %eachPart )
            if tmp[0] != 0:
                return [tmp[0], _('An error occurred when stop swap on %s :\n')%eachPart + tmp[1] ]
            else:
                print _('\n%s has been stoped.')%eachPart
                
    #安全，继续
    print '\n************************************\n'
    for eachMP in mp_config:
        targetPart = mp_config[eachMP]['part']
        targetFs = mp_config[eachMP]['fs']
        if targetFs != "current":
            # 擦除 filesystem signature 
            tmp = commands.getstatusoutput( 'wipefs -a %s' %targetPart )
            print tmp[1]
            
            #创建文件系统
            mkfs_opts = ''
            # mkfs.reiserfs is interactive unless passed a -q 
            if targetFs == "reiserfs":
                mkfs_opts = "-q"
            # mkfs.xfs will not overwrite existing filesystems unless one passes -f. 
            elif targetFs == "xfs":
                mkfs_opts="-f";
            else:
                mkfs_opts = "-q" # for jfs
                
            print _('Making %s filesystem on %s...') %( targetFs, targetPart )
            tmp = commands.getstatusoutput( 'mkfs.%s %s %s' %( targetFs, mkfs_opts, targetPart ) )
            if tmp[0] != 0:
                return [tmp[0], _('An error occurred when format %s :\n')%targetPart + tmp[1] ]
            else:
                print _('%s filesystem has been successfully maked on %s.')%(targetFs, targetPart)
            #改写分区ID。即使出错，仍然继续
            tmp = commands.getstatusoutput( 'sfdisk -c %s %s 83' %( targetPart[0:8], targetPart[8:] ) )
            if tmp[0] != 0:
                print tmp[1] + _('\nError occurred when change partition ID of %s. Not fatal. Program continue.\n')%targetPart
            else:
                print 'Partition type (Id) of %s has been changed to 83（Linux）.'%targetPart
                
    if swap_part:
        #tmp = commands.getstatusoutput( 'dd if=/dev/zero of=%s bs=1 count=512' %swap_part )
        #print tmp[1]
        #在一个 fat 或 ntfs 分区上 mkswap 之后，blkid 和 vol_id 仍然显示 fat 或 ntfs。 9.04 的 vol-id 还会告诉我，分区的 volume type 不唯一，加上 --probe-all 以后，显示既有 fat（ntfs），又有 swap。我只好先 mkfs.ext2，再 mkswap，就正确了。或者 dd 进 512 字节的 0。似乎 mkswap 不会动分区的前 512 字节（我猜想把 grub 安装到 swap 分区也是可行的）。ext3 等 linux 文件系统的前 512 字节似乎都是 0，如果不安装 grub 的话。(billbear)
        
        # 擦除 filesystem signature 
        tmp = commands.getstatusoutput( 'wipefs -a %s' %swap_part )
        print tmp[1]
        
        tmp = commands.getstatusoutput( 'mkswap %s' %swap_part )
        if tmp[0] != 0:
            return [tmp[0], _('An error occurred when mkswap %s :\n')%swap_part + tmp[1] ]
        else:
            print 'mkswap %s done.' %swap_part 

        #改写分区ID。即使出错，仍然继续
        tmp = commands.getstatusoutput( 'sfdisk -c %s %s 82' %( swap_part[0:8], swap_part[8:] ) )
        if tmp[0] != 0:
            print tmp[1] + _('\nError occurred when change partition ID of %s. Not fatal. Program continue.\n')%swap_part
        else:
            print 'Partition type (Id) of %s has been changed to 82（Linux swap）.'%swap_part

    return [ 0, 'All partitions are successfully formated.' ]






def get_mount_option( mountPoint, FS ):
    if FS == 'reiserfs' and ( mountPoint == '/boot' or mountPoint == '/') :
        return 'notail'
    elif ( FS == 'ext2'  or  FS == 'ext3'  or  FS == 'ext4' )  and  mountPoint == '/':
        return "errors=remount-ro"
    else:
        return "defaults"



def mount_a_partition( mountPoint, target_dir, mp_config ):
    #创建挂载目录
    tmp = commands.getstatusoutput( 'mkdir -p %s' %( target_dir + mountPoint ) )
    if tmp[0] != 0:
        return [tmp[0], 'mkdir -p %s' %( target_dir + mountPoint ) + _('failed：\n') + tmp[1] ]
    else:
        print '%s has been made.' %( target_dir + mountPoint )
    #要挂载的分区
    part = mp_config[mountPoint]['part']
    #文件系统
    if mp_config[mountPoint]['fs'] == 'current':
        tmp = get_uuid_fstype( part )
        if tmp[0] != 0:
            return tmp
        else:
            fs = tmp[2]
    else:
        fs = mp_config[mountPoint]['fs']
    #获取挂载参数（需用到前面获取的 part 和 fs type）
    mountOption = get_mount_option( mountPoint, fs )
    #挂载
    tmp = commands.getstatusoutput( 'mount -t %s -o %s %s %s' %( fs, mountOption, part, target_dir + mountPoint )  )
    if tmp[0] != 0:
        return [tmp[0], 'mount -t %s -o %s %s %s' %( fs, mountOption, part, target_dir + mountPoint ) + _('failed：\n') + tmp[1] ]
    else:
        msg = '%s has been mounted to %s.' %( part, target_dir + mountPoint )
        print msg
        return [0, msg]




def mount_target_partitions( target_dir, mp_config  ):
    # 即使是独立分区的 /var，启动时在 /var 被挂载前也需要有 /var/lock 和 /var/run 这两个目录。  ———— billbear
    
    # 挂载 /
    tmp = mount_a_partition( '/', target_dir, mp_config )
    if tmp[0] != 0:
        return tmp
        
    # 创建 var/lock 、var/run 目录
    tmp = commands.getstatusoutput( 'mkdir -p %s %s' %( target_dir + '/var/run', target_dir + '/var/lock' ) )
    if tmp[0] != 0:
        return [tmp[0], 'mkdir -p %s %s' %( target_dir + '/var/run', target_dir + '/var/lock' ) + _('failed：\n') + tmp[1] ]
    else:
        print '"%s" and "%s" has been made.'  %( target_dir + '/var/run', target_dir + '/var/lock' )
        
    # 处理其它挂载点
    MPs = set( [ eachMP for eachMP in mp_config ] )
    MPs.remove('/')
    for eachMP in MPs:
        tmp = mount_a_partition( eachMP, target_dir, mp_config )
        if tmp[0] != 0:
            return tmp
    
    # 所有操作都成功完成，返回
    return [ 0, '\r\nAll target partitions have been mounted successfully.\r\n' ]








def make_system_dirs( target_root ):
    print _('\nMaking system dirs ...')
    errors = []
    for each in ( '/proc', '/sys', '/tmp', '/mnt', '/media', '/media/cdrom0' ):
        tmp = commands.getstatusoutput( 'mkdir -p %s'%(target_root + each)  )
        if tmp[0] != 0:
            errors.append( _('Error occurred when mkdir %s , you need to make it manually.')%(target_root + each) )
        else:
            print _('%s has been made.')%(target_root + each)
        
    tmp = commands.getstatusoutput( 'chmod 1777 %s/tmp' %target_root )
    if tmp[0] != 0:
        errors.append( _('Error occurred when "chmod 1777 %s/tmp", you need to do it manually.')%target_root )
    else:
        print '"chmod 1777 %s/tmp" done.'%target_root

    if errors:
        return [ 1, '\n'.join( errors ) ]
    else:
        return [ 0, 'No problem.' ]


def get_uuid_fstype( part ):
    uuid = ''
    fstype = ''
    tmp = commands.getstatusoutput( 'blkid -p %s' %part )
    if tmp[0] != 0:
        return tmp
    else:
        bbb = tmp[1].split()
        for each in bbb:
            if each[0:5] == 'UUID=':
                uuid = each[6:-1]
            if each[0:5] == 'TYPE=':
                fstype = each[6:-1]
        return (0, uuid, fstype)




def generate_fstab( fstab_file, mp_config, swap_part ):
    print _('\nGenerating fstab ...')
    fstab_text = '''
# /etc/fstab: static file system information.
#
# Use 'blkid -o value -s UUID' to print the universally unique identifier
# for a device; this may be used with UUID= as a more robust way to name
# devices that works even if disks are added and removed. See fstab(5).
#
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
proc            /proc           proc    nodev,noexec,nosuid 0       0
'''
    MPs = mp_config.keys()
    MPs.sort()
    for eachMP in MPs:
        thePart = mp_config[eachMP]['part']
        # 磁盘检查参数
        if eachMP == '/':
            passOpt = '1'
        else:
            passOpt = '2'
        # 获取 UUID
        tmp = get_uuid_fstype( thePart )
        if tmp[0] != 0:
            return tmp
        else:
            uuid = tmp[1]
        # 获取文件系统
        if mp_config[eachMP]['fs'] == 'current':
            tmp = get_uuid_fstype( thePart )
            if tmp[0] != 0:
                return tmp
            else:
                fs = tmp[2]
        else:
            fs = mp_config[eachMP]['fs']
        # 获取挂载参数
        mountOpt = get_mount_option( eachMP, fs )
        # 生成挂载条目
        entry = '#%s\nUUID=%s      %s      %s      %s      0      %s\n'%(thePart, uuid, eachMP, fs, mountOpt, passOpt )
        fstab_text += entry
        
    if swap_part:
        tmp = get_uuid_fstype( swap_part )
        if tmp[0] != 0:
            return tmp
        else:
            uuid = tmp[1]
        entry = '#%s\nUUID=%s       none            swap    sw              0       0\n'%(swap_part, uuid)
        fstab_text += entry
    
    #FIXME:未加入光驱、软驱的挂载点
    
    if os.path.exists( fstab_file ):
        whatever = os.system( 'mv %s %s.bak'%( fstab_file, fstab_file ) )
    
    f = file( fstab_file, 'w' )
    f.write( fstab_text )
    f.close()

    return [ 0, 'generate_fstab done.\n' ]



def fix_resume( target_dir, swap_part ):
    if not swap_part:
        tmp = commands.getstatusoutput( './sh/fix_resume.sh %s %s' %(target_dir, 'none') )
    else:
        tmp = commands.getstatusoutput( './sh/fix_resume.sh %s %s' %(target_dir, swap_part) )
    return tmp




def change_host_name( target_dir, newHostname ):
    try:
        print '\nChanging hostname ...'
        ##########
        f = file(target_dir+'/etc/hostname', 'r')
        oldHostname = f.readline().rstrip('\n')
        f.close()
        f = file(target_dir+'/etc/hostname', 'w')
        f.write(newHostname)
        f.close()
        ##########
        f = file(target_dir+'/etc/hosts', 'r')
        aaa = ''.join( f.readlines() )
        f.close()
        aaa = aaa.replace( '\t'+oldHostname, '\t'+newHostname )
        aaa = aaa.replace( ' '+oldHostname, ' '+newHostname )  # 8.04 的 hosts 中，主机名前面不是 \t，而是空格
        f = file(target_dir+'/etc/hosts', 'w')
        f.write(aaa)
        f.close()
        ##########
        print _('Hostname han been changed successfully.')
        return [0, 'change_host_name done.' ]
    except Exception, e:
        return [1, str(e) + _('\nSorry, failed to change hostname.\n') ]




def install_grub2( target_dir, grub_dev ):
    print _('\nInstaling grub2 ...')
    cmd = './sh/install_grub.sh %s %s' %(target_dir, grub_dev)
    ret = os.system( cmd )
    if ret != 0:
        return [1, _('Sorry, failed to install grub2, you need to do it manually.\n') ]
    else:
        return [ 0, 'install_grub2 done.' ]




    
if __name__ == '__main__':
    #mp_cfg = { '/':{ 'part':'/dev/sdb4', 'fs':'reiserfs' },
    #           '/home':{ 'part':'/dev/sdb1', 'fs':'reiserfs' }
    #         }
    
    #swap_part = ''
    
    pass








��    ^           �      �     �     �       M   '     u     �     �  #   �     �     �     �     �     	     	     '	     9	  :   M	  :   �	  >   �	  -   
     0
  	   8
     B
  0   a
     �
  P   �
  <   �
  6   2     i     k     q     �     �  *   �     �  #   �  #     )   8  #   b  #   �     �     �     �  W   �  I   (  <   r  %   �      �     �  D     <   W  m   �  3     3   6  +   j  &   �     �     �     �  	   �     �  $        2  '   Q  
   y     �     �     �     �     �     �     �     �  <     I   J  E   �  -   �  >     ;   G  =   �  '   �  !   �  %     
   1  
   <     G  &   S  &   z  0   �     �  %   �          %  5  *     `     b     �  M   �     �     �          -     K     R     Z     j     w     �     �     �  F   �  F     J   K  .   �  
   �  
   �  &   �  ,        /  W   ?  F   �  2   �            $        >     N  $   j     �     �     �  #   �        &        ?     F     M  J   j  G   �  +   �  #   )      M     n  8   �  7   �  }   �  6   y  8   �  1   �          ;     H     [  	   k  3   u     �     �     �     �        &        6     C     V     ]  	   n     x  D   �  >   �  9     1   R  +   �  -   �  -   �           '   1   A      s   
   �      �   2   �   2   �   .    !  $   /!  1   T!     �!     �!         W       R   4   ?                 D   /       E   !      H   =   	      $       ]      F   A   "       U                     B      G   \                         Z             P          ,   '      [   ;          .       3   %   T   :           (   8            )   >           &               9   S   ^         Q   *      K           @   +      V      C   N       L           5      O   0       #   7   I       M   Y   X   -   2          <   6       1            
   J    
 
%s has been stoped. 
%s has been umounted. 
Error occurred when change partition ID of %s. Not fatal. Program continue.
 
Generating fstab ... 
Instaling grub2 ... 
Making system dirs ... 
Sorry, failed to change hostname.
              
    Browse...       Cancel       Close       Start Backup       Start Clone       Start Restore      -->  Create ext3 filesystem. All data will be destroyed!   -->  Create ext4 filesystem. All data will be destroyed!   -->  Create reiserfs filesystem. All data will be destroyed!   -->  Do NOT format. Use current filesystem.   Add     Reset    Refresh
 partition 
     list %s filesystem has been successfully maked on %s. %s has been made. %s will be formated as %s (All data in it will be destroyed!) and mounted to %s
 %s will be used as swap (All data in it will be destroyed!)
 %s will use current filesystem, and be mounted to %s 
 / /home <b> Excludes </b> <b> Others </b> <b> System Image File </b> <b> Target partitions and file system </b> Adding system dirs ... An error occurred when format %s :
 An error occurred when mkswap %s :
 An error occurred when stop swap on %s :
 An error occurred when umount %s :
 Backing up current system to %s...
 Backup Clone Cpoying system files...
 Current system will be backup to %s. If there is any disk in CD-ROM, please remove it.
 Dnoe. The size of the squashfs-image-file to be generated is about %s MB. Done. The size of the data to be transported is about %s MB. ERROR: "restore_from" is unspecified. ERROR: backup_to is unspecified. ERROR: mode is unspecified. Error occurred when "chmod 1777 %s/tmp", you need to do it manually. Error occurred when mkdir %s , you need to make it manually. Error: "squashfs-tools" is needed to backup system. Ues "sudo apt-get install squashfs-tools" to install it.
 Error: %s is assigned repeatedly to "%s" and "%s".
 Error: %s is assigned repeatedly to "%s" and swap.
 Error: filesystem for "%s" is unspecified.
 Error: root partition is unspecified.
 Estimate Size Estimate size Estimating... File name GRUB will NOT be installed
 Grub2 han been set up successfully.
 Grub2 will be installed to %s
 Hostname han been changed successfully. Image File Install GRUB to  Making %s filesystem on %s... New host name Program stoped. Restore Restoring ...
 Save to Shutdown when task completes Sorry, failed to install grub2, you need to do it manually.
 Sorry, fix_resume failed. System will not be able to hibernate properly.
 Starting clone...

If there is any disk in CD-ROM, please remove it.
 System files have been copied. Continuing...
 System has been backed up. %d minutes and %d seconds elapsed.
 System has been cloned. %d minutes and %d seconds elapsed.
 System has been restored. %d minutes and %d seconds elapsed.
 System will shutdown in %s seconds...   The hostname will be set as "%s"
 check_target_partitions error, exit.
 continue ? failed：
 failed：

 format_target_partitions error, exit.
 functions.generate_fstab error, exit.
 mksquashfs error when adding system dirs. Exit.
 mksquashfs error. Exit.
 mount_target_partitions error, exit.
 rsync error. Exit.
 swap Project-Id-Version: UCloner 10.10.1
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2010-11-14 15:54+0800
PO-Revision-Date: 2010-10-20 12:05+0800
Last-Translator: pt <ptptptptptpt@163.com>
Language-Team: Chinese (simplified)
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
 
 
交换分区 %s 已停用。 
%s 已挂载。 
改写 %s 的分区ID时有错误发生，但不严重，程序将继续。
 
正在生成 fstab ... 
正在安装 grub2 ... 
正在创建系统目录 ... 
更改主机名时出错。
              
    浏览...       取消       关闭       开始备份       开始克隆       开始恢复      -->  创建 ext3 文件系统，分区中所有数据将被摧毁！   -->  创建 ext4 文件系统，分区中所有数据将被摧毁！   -->  创建 reiserfs 文件系统，分区中所有数据将被摧毁！   -->  不格式化，使用现有文件系统   增加     重设      刷新   
   分区   
   列表    %s 文件系统创建成功（位于%s）。 %s 已创建。 %s 将被格式化为 %s （分区中所有数据将被摧毁！），挂载点为 %s 
 %s 将被用作交换分区（分区中所有数据将被摧毁！）
 %s 将使用现有文件系统，挂载点为 %s 
 / /home <b> 排除以下文件和目录 </b> <b> 其它 </b> <b> 系统映像文件 </b> <b> 目标分区和文件系统 </b> 正在添加系统目录 ... 格式化 %s 时出错：
 mkswap %s 出错：
 停用交换分区 %s 时出错：
 挂载 %s 时出错：
 正在将当前系统备份到 %s ...
 备份 克隆 开始复制系统文件...
 将把当前系统备份为 %s 。光驱中如果有光盘，请取出。
 估算完毕。将生成大小约为 %s MB 的 squashfs 映像文件。 估算完毕。将传送约 %s MB 数据。 错误：未指定"restore_from"。 错误：未指定 backup_to 。 错误：未指定 mode 。 "chmod 1777 %s/tmp" 出错，您需要手动执行它。 创建 %s 目录时出错，您需要手动创建它。 错误：需要先安装 squashfs-tools 才能备份系统。可用如下命令安装：sudo apt-get install squashfs-tools 
 错误: %s 被同时指定为 "%s" 和 "%s" 分区。
 错误：%s 被同时指定为 "%s" 和 交换分区。
 错误：未指定用于 "%s" 的文件系统。
 错误：未指定 / 分区。
 估算体积    估算体积    正在估算... 文件名 GRUB 将不被安装，您需要手动设置引导
 Grub2 安装成功。
 Grub2 将被安装至 %s
 更改主机名成功。 映像文件 GRUB 安装至 正在创建 %s 文件系统于 %s ... 新主机名 程序已停止。 恢复 开始恢复...
 保存至 任务完成后自动关机 很抱歉，安装 grub2 时出错，您需要手动设置引导。
 很抱歉, fix_resume 失败，系统将无法正常休眠。
 开始克隆...

光驱中如果有光盘，请取出。
 系统文件复制完毕，执行后续操作...
 系统备份完毕，耗时 %d 分 %d 秒 
 系统克隆完毕，耗时 %d 分 %d 秒。
 系统恢复完毕，耗时 %d 分 %d 秒。
 %s 秒后自动关机...   主机名将被设为 %s
 check_target_partitions 出错，程序中止。
 要继续吗？ 失败：
 失败：

 format_target_partitions 出错，程序中止。
 functions.generate_fstab 出错，程序中止。
 添加系统目录时出错，程序中止。
 mksquashfs 出错，程序中止。
 mount_target_partitions 出错，程序中止。
 rsync 出错，程序中止。
 swap 
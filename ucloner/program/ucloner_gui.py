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


import gtk
import os
import vte
import sys
import commands
import time
import signal

import ucloner_cmd
import functions






import gettext
APP_NAME="ucloner"
LOCALE_DIR=os.path.abspath("locale")
if not os.path.exists(LOCALE_DIR):
    LOCALE_DIR="/usr/share/locale"
gettext.bindtextdomain(APP_NAME, LOCALE_DIR)
gettext.textdomain(APP_NAME)
_ = gettext.gettext




import gtk.glade
gtk.glade.bindtextdomain(APP_NAME, LOCALE_DIR)
gtk.glade.textdomain(APP_NAME)




class MainWindow(object):
    def __init__(self, parent=None):
    
        self.VERSION = '10.10.1'
        
        self.programDir = os.path.split( os.path.realpath( sys.argv[0] ) )[0]

        ###### 排除目录 ######
        self.exclude_default = ucloner_cmd.get_default_excludes()
        self.exclude_user = []


        ##### 列表：目标分区、文件系统、grub设备  ######        
        self.liststore_partitions = gtk.ListStore(str, str)
        
        self.liststore_fstype = gtk.ListStore(str, str)
        self.liststore_fstype.append( [ 'current', _('  -->  Do NOT format. Use current filesystem.') ] )
        self.liststore_fstype.append( [ 'ext4', _('  -->  Create ext4 filesystem. All data will be destroyed!') ] )
        self.liststore_fstype.append( [ 'ext3', _('  -->  Create ext3 filesystem. All data will be destroyed!') ] )
        self.liststore_fstype.append( [ 'reiserfs', _('  -->  Create reiserfs filesystem. All data will be destroyed!') ] )

        
        self.liststore_grubdev = gtk.ListStore(str)
        

        
        
        ###### 主窗口 ######
        self.gladefile = "./glade/gui.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        
        self.main_win = self.builder.get_object('window1')
        self.main_win.connect('destroy', gtk.main_quit)        
        self.main_win.set_title('UCloner ' + self.VERSION)
        #self.main_win.set_icon_from_file('ucloner.png')
        self.main_win.set_position(gtk.WIN_POS_CENTER)
        self.main_win.set_resizable(False)




        
        ############ 克隆  ############
        
        self.textview_excludes_clone = self.builder.get_object('textview_excludes_clone')
        
        self.button_add_clone = self.builder.get_object('button_add_clone')
        self.button_add_clone.connect('clicked', self.on_button_add_clicked,'clone' )
        
        self.button_reset_clone = self.builder.get_object('button_reset_clone')
        self.button_reset_clone.connect('clicked', self.on_button_reset_clicked,'clone' )
        
        self.button_estimate_clone = self.builder.get_object('button_estimate_clone')
        self.button_estimate_clone.connect('clicked', self.on_button_estimate_clicked,'clone' )
        

        self.comboboxentry_root_clone = self.builder.get_object('comboboxentry_root_clone')       
        self.comboboxentry_root_clone.set_model(self.liststore_partitions)
        self.comboboxentry_root_clone.set_text_column(0)
        cell_1_root_clone = gtk.CellRendererText()
        self.comboboxentry_root_clone.pack_start(cell_1_root_clone, True)
        self.comboboxentry_root_clone.add_attribute(cell_1_root_clone, 'text', 1)

        self.comboboxentry_root_clone.child.connect("changed", self.on_root_part_changed, 'clone')

        self.comboboxentry_home_clone = self.builder.get_object('comboboxentry_home_clone')
        self.comboboxentry_home_clone.set_model(self.liststore_partitions)
        self.comboboxentry_home_clone.set_text_column(0)
        cell_1_home_clone = gtk.CellRendererText()
        self.comboboxentry_home_clone.pack_start(cell_1_home_clone, True)
        self.comboboxentry_home_clone.add_attribute(cell_1_home_clone, 'text', 1)

        self.comboboxentry_swap_clone = self.builder.get_object('comboboxentry_swap_clone')
        self.comboboxentry_swap_clone.set_model(self.liststore_partitions)
        self.comboboxentry_swap_clone.set_text_column(0)
        cell_1_swap_clone = gtk.CellRendererText()
        self.comboboxentry_swap_clone.pack_start(cell_1_swap_clone, True)
        self.comboboxentry_swap_clone.add_attribute(cell_1_swap_clone, 'text', 1)
        

        self.comboboxentry_rootfs_clone = self.builder.get_object('comboboxentry_rootfs_clone')
        self.comboboxentry_rootfs_clone.set_model(self.liststore_fstype)
        self.comboboxentry_rootfs_clone.set_text_column(0)
        cell_1_rootfs_clone = gtk.CellRendererText()
        self.comboboxentry_rootfs_clone.pack_start(cell_1_rootfs_clone, True)
        self.comboboxentry_rootfs_clone.add_attribute(cell_1_rootfs_clone, 'text', 1)
        
        
        self.comboboxentry_homefs_clone = self.builder.get_object('comboboxentry_homefs_clone')
        self.comboboxentry_homefs_clone.set_model(self.liststore_fstype)
        self.comboboxentry_homefs_clone.set_text_column(0)
        cell_1_homefs_clone = gtk.CellRendererText()
        self.comboboxentry_homefs_clone.pack_start(cell_1_homefs_clone, True)
        self.comboboxentry_homefs_clone.add_attribute(cell_1_homefs_clone, 'text', 1)
        
        
        self.button_refresh_clone = self.builder.get_object('button_refresh_clone')
        self.button_refresh_clone.connect('clicked', self.on_button_refresh_clicked )


        self.comboboxentry_grubdev_clone = self.builder.get_object('comboboxentry_grubdev_clone')
        self.comboboxentry_grubdev_clone.set_model(self.liststore_grubdev)
        self.comboboxentry_grubdev_clone.set_text_column(0)

        self.entry_new_hostname_clone = self.builder.get_object('entry_new_hostname_clone')
        
        self.button_start_clone = self.builder.get_object('button_start_clone')
        self.button_start_clone.connect('clicked', self.on_button_start_clone_clicked )




        ############ 备份  ############

        # 保存路径
        self.entry_backup_dir = self.builder.get_object('entry_backup_dir')
        self.entry_backup_filename = self.builder.get_object('entry_backup_filename')
        # 浏览...
        self.button_browse_backup = self.builder.get_object('button_browse_backup')
        self.button_browse_backup.connect('clicked', self.on_button_browse_backup_clicked )

        # 排除目录
        self.textview_excludes_backup = self.builder.get_object('textview_excludes_backup')
        
        self.button_add_backup = self.builder.get_object('button_add_backup')
        self.button_add_backup.connect('clicked', self.on_button_add_clicked, 'backup')
        
        self.button_reset_backup = self.builder.get_object('button_reset_backup')
        self.button_reset_backup.connect('clicked', self.on_button_reset_clicked, 'backup' )
        
        self.button_estimate_backup = self.builder.get_object('button_estimate_backup')
        self.button_estimate_backup.connect('clicked', self.on_button_estimate_clicked,'backup' )

        self.button_start_backup = self.builder.get_object('button_start_backup')
        self.button_start_backup.connect('clicked', self.on_button_start_backup_clicked )
        
        
        
        

        ############ 恢复 ############

        # 从文件恢复
        self.entry_restore_from = self.builder.get_object('entry_restore_from')
        # 浏览...
        self.button_browse_restore = self.builder.get_object('button_browse_restore')
        self.button_browse_restore.connect('clicked', self.on_button_browse_restore_clicked )


        # 目标分区
        self.comboboxentry_root_restore = self.builder.get_object('comboboxentry_root_restore')       
        self.comboboxentry_root_restore.set_model(self.liststore_partitions)
        self.comboboxentry_root_restore.set_text_column(0)
        cell_1_root_restore = gtk.CellRendererText()
        self.comboboxentry_root_restore.pack_start(cell_1_root_restore, True)
        self.comboboxentry_root_restore.add_attribute(cell_1_root_restore, 'text', 1)

        self.comboboxentry_root_restore.child.connect("changed", self.on_root_part_changed, 'restore')

        self.comboboxentry_home_restore = self.builder.get_object('comboboxentry_home_restore')
        self.comboboxentry_home_restore.set_model(self.liststore_partitions)
        self.comboboxentry_home_restore.set_text_column(0)
        cell_1_home_restore = gtk.CellRendererText()
        self.comboboxentry_home_restore.pack_start(cell_1_home_restore, True)
        self.comboboxentry_home_restore.add_attribute(cell_1_home_restore, 'text', 1)

        self.comboboxentry_swap_restore = self.builder.get_object('comboboxentry_swap_restore')
        self.comboboxentry_swap_restore.set_model(self.liststore_partitions)
        self.comboboxentry_swap_restore.set_text_column(0)
        cell_1_swap_restore = gtk.CellRendererText()
        self.comboboxentry_swap_restore.pack_start(cell_1_swap_restore, True)
        self.comboboxentry_swap_restore.add_attribute(cell_1_swap_restore, 'text', 1)
        

        self.comboboxentry_rootfs_restore = self.builder.get_object('comboboxentry_rootfs_restore')
        self.comboboxentry_rootfs_restore.set_model(self.liststore_fstype)
        self.comboboxentry_rootfs_restore.set_text_column(0)
        cell_1_rootfs_restore = gtk.CellRendererText()
        self.comboboxentry_rootfs_restore.pack_start(cell_1_rootfs_restore, True)
        self.comboboxentry_rootfs_restore.add_attribute(cell_1_rootfs_restore, 'text', 1)
        
        
        self.comboboxentry_homefs_restore = self.builder.get_object('comboboxentry_homefs_restore')
        self.comboboxentry_homefs_restore.set_model(self.liststore_fstype)
        self.comboboxentry_homefs_restore.set_text_column(0)
        cell_1_homefs_restore = gtk.CellRendererText()
        self.comboboxentry_homefs_restore.pack_start(cell_1_homefs_restore, True)
        self.comboboxentry_homefs_restore.add_attribute(cell_1_homefs_restore, 'text', 1)
        
        
        self.button_refresh_restore = self.builder.get_object('button_refresh_restore')
        self.button_refresh_restore.connect('clicked', self.on_button_refresh_clicked )


        self.comboboxentry_grubdev_restore = self.builder.get_object('comboboxentry_grubdev_restore')
        self.comboboxentry_grubdev_restore.set_model(self.liststore_grubdev)
        self.comboboxentry_grubdev_restore.set_text_column(0)

        self.entry_new_hostname_restore = self.builder.get_object('entry_new_hostname_restore')

        self.button_start_restore = self.builder.get_object('button_start_restore')
        self.button_start_restore.connect('clicked', self.on_button_start_restore_clicked )



        ##### 初始化 ######
        self.entry_backup_filename.set_text( time.strftime('%Y-%m-%d_%H%M%S') + '.squashfs' )
        self.refresh_textview_excludes()
        self.comboboxentry_rootfs_restore.set_active(0)
        self.comboboxentry_homefs_restore.set_active(0)
        self.comboboxentry_rootfs_clone.set_active(0)
        self.comboboxentry_homefs_clone.set_active(0)
        
        self.main_win.show_all()


    # 刷新显示 排除目录 
    def refresh_textview_excludes(self):
        text_buffer = gtk.TextBuffer()
        text_buffer.set_text( '\n'.join( self.exclude_user + self.exclude_default ) )
        self.textview_excludes_clone.set_buffer(text_buffer)
        self.textview_excludes_backup.set_buffer(text_buffer)

    # 增加排除目录
    def on_button_add_clicked(self, widget, data ):
        dialog = gtk.FileChooserDialog('UCloner', None, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, 
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK,  gtk.RESPONSE_OK))
        res = dialog.run()
        if res == gtk.RESPONSE_OK:
            self.exclude_user.append( dialog.get_filename() )
        dialog.destroy()
        self.refresh_textview_excludes()
        
    # 重设
    def on_button_reset_clicked(self, widget, data ):
        self.exclude_user = []
        self.refresh_textview_excludes()


    # 将排除目录写入文件待用
    def write_excludes_to_file(self):
        f = file('./excludes','w')
        f.write( '\n'.join( self.exclude_default ) + '\n' + '\n'.join( self.exclude_user ) )
        f.close()

    # 估算体积
    def on_button_estimate_clicked(self, widget, data ):
        self.main_win.set_sensitive(False)
        self.init_sub_win()
        self.sub_win.set_title( _('Estimate Size') )
        self.write_excludes_to_file()
        cmd = '%s/estimate_size.py'%self.programDir
        if data == 'clone':
            self.id_subproc = self.vte1.fork_command(command=cmd, argv=[cmd, 'clone', './excludes'])
        elif data == 'backup':
            self.id_subproc = self.vte1.fork_command(command=cmd, argv=[cmd, 'backup', './excludes'])
        else:
            pass


    # 列出分区
    def on_button_refresh_clicked(self, widget ):
        self.liststore_partitions.clear()
        self.liststore_partitions.append( ['', 'Do not use a separate partition.'] )
        HDs = commands.getoutput('echo /dev/[hs]d[a-z]').split()
        for each_hd in HDs:
            ret = commands.getstatusoutput("parted -s %s unit B  print | grep -e '^[ ,0-9][0-9]' | grep -v 'extended' " %each_hd)
            if ( ret[0] != 0 ) or ( not ret[1] ) :
                pass
            else:
                for each_line in ret[1].split('\n'):
                    details = []
                    aaa = each_line.split()
                    size_B = int( aaa[3][0:-1] )
                    size_G = str( size_B/1073741824 ) + '.' + str( (size_B % 1073741824) / 107374182 ) + ' GB'
                    details.append( size_G )
                    partNO = aaa[0]
                    tmp = commands.getstatusoutput( 'blkid -p %s'%(each_hd + partNO) )
                    if tmp[0] == 0:
                        bbb = tmp[1].split()
                        bbb.sort()
                        for each in bbb:
                            if each[0:5] == 'LABEL':
                                details.append( each )
                            if each[0:4] == 'TYPE':
                                details.append( each )
                            if each[0:7] == 'VERSION':
                                details.append( each )
                    self.liststore_partitions.append( [ each_hd + partNO,  '   ' + ',   '.join(details) + '   ' ] )

        self.liststore_partitions.append( ['', 'Do not use a separate partition.'] )



    # grub 设备选单
    def on_root_part_changed(self, widget, data ):
        if data == 'clone':
            dev1 = self.comboboxentry_root_clone.child.get_text()
        if data == 'restore':
            dev1 = self.comboboxentry_root_restore.child.get_text()
        
        if len(dev1) >= 9:
            dev0 = dev1[0:8]
            self.liststore_grubdev.clear()
            self.liststore_grubdev.append( [ '' ] )
            self.liststore_grubdev.append( [ dev0 ] )
            self.liststore_grubdev.append( [ dev1 ] )
            
            self.comboboxentry_grubdev_clone.set_active(0)
            self.comboboxentry_grubdev_restore.set_active(0)
        else:
            self.liststore_grubdev.clear()



    # 获取所有参数
    def get_all_args(self):
        self.root_part_clone = self.comboboxentry_root_clone.child.get_text()
        self.root_part_fs_clone = self.comboboxentry_rootfs_clone.child.get_text()
        self.home_part_clone = self.comboboxentry_home_clone.child.get_text()
        self.home_part_fs_clone = self.comboboxentry_homefs_clone.child.get_text()
        self.swap_part_clone = self.comboboxentry_swap_clone.child.get_text()
        self.grub_device_clone = self.comboboxentry_grubdev_clone.child.get_text()
        self.new_hostname_clone = self.entry_new_hostname_clone.get_text()
        
        saveDir = self.entry_backup_dir.get_text()
        fileName = self.entry_backup_filename.get_text()
        if saveDir and fileName:
            self.backup_to = os.path.join(saveDir, fileName)
        else:
            self.backup_to = ''
            
        self.restore_from = self.entry_restore_from.get_text()
        
        self.root_part_restore = self.comboboxentry_root_restore.child.get_text()
        self.root_part_fs_restore = self.comboboxentry_rootfs_restore.child.get_text()
        self.home_part_restore = self.comboboxentry_home_restore.child.get_text()
        self.home_part_fs_restore = self.comboboxentry_homefs_restore.child.get_text()
        self.swap_part_restore = self.comboboxentry_swap_restore.child.get_text()
        self.grub_device_restore = self.comboboxentry_grubdev_restore.child.get_text()
        self.new_hostname_restore = self.entry_new_hostname_restore.get_text()
        


    # 初始化子窗口
    def init_sub_win(self):

        self.builder2 = gtk.Builder()
        self.builder2.add_from_file("./glade/gui2.glade")
        
        self.sub_win = self.builder2.get_object('window1')
        self.sub_win.connect('destroy', self.on_sub_win_closed)
        self.sub_win.set_title('UCloner')
        #self.sub_win.set_icon_from_file('ucloner.png')
        self.sub_win.set_position(gtk.WIN_POS_CENTER)
        self.sub_win.set_resizable(True)

        self.vte1 = vte.Terminal()
        self.vte1.set_size_request(720, 420)
        self.vte1.set_cursor_blinks(False)
        self.vte1.connect ("child-exited", self.on_vte_exit, None)

        scrollbar = gtk.VScrollbar()
        adjustment = self.vte1.get_adjustment()
        scrollbar.set_adjustment(adjustment)
        
        hbox_vte = self.builder2.get_object('hbox_vte')
        hbox_vte.pack_start(self.vte1)
        hbox_vte.pack_start(scrollbar, expand=False)
        
        self.checkbutton_auto_shutdown = self.builder2.get_object('checkbutton_auto_shutdown')
        
        self.button_stop_task = self.builder2.get_object('button_stop_task')
        self.button_stop_task.connect('clicked', self.stop_task )

        self.button_close_subwin = self.builder2.get_object('button_close_subwin')
        self.button_close_subwin.set_sensitive(False)
        self.button_close_subwin.connect('clicked', self.close_subwin )

        self.sub_win.show_all()
        


    def on_sub_win_closed(self, widget):
        self.main_win.set_sensitive(True)
        try:
            os.kill( self.id_subproc, signal.SIGKILL )
        except:
            pass
            

    def stop_task(self, widget):
        try:
            os.kill( self.id_subproc, signal.SIGKILL )
        except:
            pass
            


    def close_subwin(self, widget):
        self.sub_win.destroy()
            

    def on_vte_exit(self, vte, data):
        self.button_stop_task.set_sensitive(False)
        self.button_close_subwin.set_sensitive(True)
        
        status = self.vte1.get_child_exit_status()
        # 若正常退出
        if status == 0:
            if self.checkbutton_auto_shutdown.get_active():
                self.vte1.feed('\r\n\n')
                self.button_stop_task.set_sensitive(True)
                self.button_close_subwin.set_sensitive(False)
                cmd = '%s/auto_shutdown.py'%self.programDir
                self.id_subproc = self.vte1.fork_command( command=cmd, argv=[cmd,] )

        # 若异常退出 或 被用户中止
        else:
            self.vte1.feed('\r\n\n' + _('Program stoped.'))
            self.checkbutton_auto_shutdown.set_active(False)



            
            


    # 开始克隆
    def on_button_start_clone_clicked(self, widget ):
        self.main_win.set_sensitive(False)
        self.init_sub_win()

        self.get_all_args()
        self.write_excludes_to_file()

        args = []
        args.append( "lang=cn" )
        args.append( "mode=clone" )
        
        if self.root_part_clone:
            args.append( "/=" + self.root_part_clone )
        if self.root_part_fs_clone:
            args.append( "/_fs=" + self.root_part_fs_clone )
        if self.home_part_clone:
            args.append( "/home=" + self.home_part_clone )
        if self.home_part_fs_clone:
            args.append( "/home_fs=" + self.home_part_fs_clone )
        if self.swap_part_clone:
            args.append( "swap=" + self.swap_part_clone )
        if self.grub_device_clone:
            args.append( "grubdev=" + self.grub_device_clone )
        if self.new_hostname_clone:
            args.append( "newhostname=" + self.new_hostname_clone )
            
        args.append( 'called_by_gui' )
        
        self.sub_win.set_title( _('Clone') )
        
        cmd = '%s/ucloner_cmd.py'%self.programDir
        self.id_subproc = self.vte1.fork_command( command=cmd, argv=[cmd,] + args )
        


    # 指定映像文件保存目录
    def on_button_browse_backup_clicked(self, widget ):
        dialog = gtk.FileChooserDialog('UCloner', None, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, 
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK,  gtk.RESPONSE_OK))
        res = dialog.run()
        if res == gtk.RESPONSE_OK:
            self.entry_backup_dir.set_text( dialog.get_filename().rstrip('/') + '/' )
        dialog.destroy()


    # 开始备份
    def on_button_start_backup_clicked(self, widget ):
        self.main_win.set_sensitive(False)
        self.init_sub_win()
        
        self.get_all_args()
        self.write_excludes_to_file()

        args = []
        args.append( "lang=cn" )
        args.append( "mode=backup" )
        args.append( "backup_to=%s"%self.backup_to )
            
        args.append( 'called_by_gui' )
        
        self.sub_win.set_title( _('Backup') )
        
        cmd = '%s/ucloner_cmd.py'%self.programDir
        self.id_subproc = self.vte1.fork_command( command=cmd, argv=[cmd,] + args )



    # 指定恢复文件
    def on_button_browse_restore_clicked(self, widget ):
        dialog = gtk.FileChooserDialog('UCloner', None, gtk.FILE_CHOOSER_ACTION_OPEN, 
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK,  gtk.RESPONSE_OK))
        res = dialog.run()
        if res == gtk.RESPONSE_OK:
            self.entry_restore_from.set_text( dialog.get_filename() )
        dialog.destroy()





    # 开始恢复
    def on_button_start_restore_clicked(self, widget ):
        self.main_win.set_sensitive(False)
        self.init_sub_win()

        self.get_all_args()

        args = []
        args.append( "lang=cn" )
        args.append( "mode=restore" )
        args.append( "restore_from=%s"%self.restore_from )
        
        if self.root_part_restore:
            args.append( "/=" + self.root_part_restore )
        if self.root_part_fs_restore:
            args.append( "/_fs=" + self.root_part_fs_restore )
        if self.home_part_restore:
            args.append( "/home=" + self.home_part_restore )
        if self.home_part_fs_restore:
            args.append( "/home_fs=" + self.home_part_fs_restore )
        if self.swap_part_restore:
            args.append( "swap=" + self.swap_part_restore )
        if self.grub_device_restore:
            args.append( "grubdev=" + self.grub_device_restore )
        if self.new_hostname_restore:
            args.append( "newhostname=" + self.new_hostname_restore )
            
        args.append( 'called_by_gui' )
        
        self.sub_win.set_title( _('Restore') )
        
        cmd = '%s/ucloner_cmd.py'%self.programDir
        self.id_subproc = self.vte1.fork_command( command=cmd, argv=[cmd,] + args )





    
if __name__ == '__main__':
    win = MainWindow();
    gtk.main()








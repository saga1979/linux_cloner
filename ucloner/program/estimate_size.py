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



import gettext
APP_NAME="ucloner"
LOCALE_DIR=os.path.abspath("locale")
if not os.path.exists(LOCALE_DIR):
    LOCALE_DIR="/usr/share/locale"
gettext.bindtextdomain(APP_NAME, LOCALE_DIR)
gettext.textdomain(APP_NAME)
_ = gettext.gettext



if len(sys.argv) < 3:
    print 'args: estimate_size.py  { backup | clone }  exclude_from\n'
    sys.exit(1)

if sys.argv[1] != 'backup' and sys.argv[1] != 'clone':
    print 'args: estimate_size.py  { backup | clone }  exclude_from\n'
    sys.exit(1)
    
if not os.path.isfile( sys.argv[2] ):
    print 'error: %s is not a file.\n'%sys.argv[2]
    sys.exit(1)


# 将所有以 /var/cache/apt 开头的项，用一个 /var/cache/apt 代替，以加快 du 速度。

newText = []
f = file( sys.argv[2], 'r' )
for eachLine in f:
    if len(eachLine) >= 14 and eachLine[0:14] == '/var/cache/apt':
        #print eachLine,
        continue
    newText.append(eachLine)
f.close()
# print newText
f = file( '/tmp/estimate_size_excludes', 'w' )
f.write( '/var/cache/apt\n' )
for each in newText:
    f.write( each )
f.close()


print _('Estimating...')


cmd = 'du -c --bytes --exclude-from="/tmp/estimate_size_excludes"  /  2>>/dev/null  | tail --lines 1 '
curspaceusage = commands.getoutput( cmd ).split()[0]


sizeClone = int(curspaceusage) / 1048576
sizeBackup = sizeClone * 2/5

print ''

if sys.argv[1] == 'backup':
    print _('Dnoe. The size of the squashfs-image-file to be generated is about %s MB.')%sizeBackup
elif sys.argv[1] == 'clone':
    print _('Done. The size of the data to be transported is about %s MB.')%sizeClone
else:
    pass





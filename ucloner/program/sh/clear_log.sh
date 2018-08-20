#!/bin/sh

find /var/log -regex '.*?[0-9].*?' -exec rm -v {} \;

find /var/log -type f | while read file
do
        cat /dev/null | tee $file
done

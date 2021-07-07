#!/usr/bin/bash

mkdir /media/usb
mount /dev/added_usb /media/usb

cp -i /var/log/boot.log /media/usb/logs/boot.log
cp -i /var/log/dmesg /media/usb/logs/dmesg.log

umount /media/usb
rm -r /media/usb

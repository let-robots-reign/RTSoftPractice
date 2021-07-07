#!/bin/bash

mkdir -p /mount/${ID_FS_UUID}
sudo /usr/bin/mount UUID=${ID_FS_UUID} /mount/${ID_FS_UUID}

LOGS_DIR=/mount/${ID_FS_UUID}/LINUX_LOGS
mkdir ${LOGS_DIR}
cp /var/log/boot.log ${LOGS_DIR}
cp /var/log/dmesg ${LOGS_DIR}

sync /mount/${ID_FS_UUID}
sudo /usr/bin/umount /mount/${ID_FS_UUID}
rm -r /mount/${ID_FS_UUID}

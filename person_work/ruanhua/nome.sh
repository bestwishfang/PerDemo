#!/bin/bash
systemctl start docker.service
systemctl start smb.service

docker login 100.95.233.94 -u admin -pHarbor12345
modprobe tipc
modprobe squashfs

umount /opt/home/Software
mount "//hghrnd-fs/hgh01/DCP_Galaxy_GX_F/br_scp_hssp_master/current/MATRIX" /opt/home/Software -o username=用户名,password=密码,rw --verbose

cd /opt/home/
nohup swift &

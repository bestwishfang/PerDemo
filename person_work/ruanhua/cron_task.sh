#!/bin/bash
# 修改/root/version/d**.cc的文件名，用于日志上传
filename=d`date "+%m%d"`.cc
rm -rf /root/version/*
touch /root/version/$filename

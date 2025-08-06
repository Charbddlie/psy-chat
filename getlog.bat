@echo off

REM 获取服务器数据
ssh root@8.153.195.92 "cd /root/psy-chat/backend && /root/miniconda3/bin/python summary.py"
scp root@8.153.195.92:/root/psy-chat/backend/log/summary* ./log/
@REM scp -r root@8.153.195.92:/root/psy-chat/backend/log/ ./
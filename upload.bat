@echo off

cd psy-front
call npm run build
cd ..

REM 上传 prompt
scp -r backend\prompt\ root@8.153.195.92:/root/psy-chat/backend/

REM 上传 backend 文件夹下的所有文件（不包括子文件夹和文件夹本身）
scp backend\*.* root@8.153.195.92:/root/psy-chat/backend/

REM 上传 psy-front/dist 文件夹及其内容（包括子文件夹和文件）
scp -r psy-front\dist root@8.153.195.92:/root/psy-chat/psy-front/

REM 上传脚本
scp *.sh root@8.153.195.92:/root/psy-chat/

echo 上传完成

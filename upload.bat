@echo off

cd psy-front
call npm run build
cd ..

REM �ϴ� prompt
scp -r backend\prompt\ root@8.153.195.92:/root/psy-chat/backend/

REM �ϴ� backend �ļ����µ������ļ������������ļ��к��ļ��б���
scp backend\*.* root@8.153.195.92:/root/psy-chat/backend/

REM �ϴ� psy-front/dist �ļ��м������ݣ��������ļ��к��ļ���
scp -r psy-front\dist root@8.153.195.92:/root/psy-chat/psy-front/

REM �ϴ��ű�
scp *.sh root@8.153.195.92:/root/psy-chat/

echo �ϴ����

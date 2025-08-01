#!/bin/bash

ssh root@8.153.195.92 "cd /root/psy-chat/backend && python3 summary.py"
scp -r root@8.153.195.92:/root/psy-chat/backend/log/ ./
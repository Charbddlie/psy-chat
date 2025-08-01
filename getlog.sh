#!/bin/bash

# 检测操作系统类型
OS_TYPE="$(uname)"
if [[ "$OS_TYPE" == "Darwin" ]]; then
    # macOS
    echo "Detected macOS"
    ssh root@8.153.195.92 "cd /root/psy-chat/backend && python3 summary.py"
    scp -r root@8.153.195.92:/root/psy-chat/backend/log/ ./
elif [[ "$OS_TYPE" == "Linux" ]]; then
    # Linux
    echo "Detected Linux"
    ssh root@8.153.195.92 "cd /root/psy-chat/backend && python3 summary.py"
    scp -r root@8.153.195.92:/root/psy-chat/backend/log/ ./
else
    echo "Unsupported OS: $OS_TYPE"
    exit 1
fi

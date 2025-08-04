import os
import tomli
import json
import asyncio
import websockets

# 读取日志目录
with open('settings.toml', 'rb') as f:
    LOG_DIR = tomli.load(f).get('log_dir', 'log')
os.makedirs(LOG_DIR, exist_ok=True)
INFO_TSV_PATH = os.path.join(LOG_DIR, "info.tsv")

# 校验字段的工具函数
def check_required_fields(data, required_fields):
    for field in required_fields:
        if field not in data:
            return field
    return None

async def handle_submit(data, user_id):
    required_fields = [
        "user_name", "age", "gender", "major", "grade", "aiAttitude", "time"
    ]
    missing = check_required_fields(data, required_fields)
    if missing:
        return {"type": "error", "msg": f"缺少字段: {missing}"}
    # write_header = not os.path.exists(INFO_TSV_PATH)
    # with open(INFO_TSV_PATH, "a", encoding="utf-8") as f:
    #     if write_header:
    #         f.write('\t'.join(required_fields) + '\n')
    #     f.write('\t'.join([str(data[k]).replace('\t', ' ') for k in required_fields]) + '\n')
    dir_name = f"{data['user_name']}_{user_id}"
    dir_path = os.path.join(LOG_DIR, dir_name)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, "info.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"type": "success", "user_name": data['user_name']}

async def handle_post_questionnaire(data, user_id):
    required_fields = ["user_name"]
    missing = check_required_fields(data, required_fields)
    if missing:
        return {"type": "error", "msg": f"缺少字段: {missing}"}
    dir_name = f"{data['user_name']}_{user_id}"
    dir_path = os.path.join(LOG_DIR, dir_name)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, "post.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"type": "success", "user_name": data['user_name']}

async def handle_pre_questionnaire(data, user_id):
    required_fields = [
        "user_name"
    ]
    missing = check_required_fields(data, required_fields)
    if missing:
        return {"type": "error", "msg": f"缺少字段: {missing}"}
    dir_name = f"{data['user_name']}_{user_id}"
    dir_path = os.path.join(LOG_DIR, dir_name)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, "pre.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"type": "success", "user_name": data['user_name']}


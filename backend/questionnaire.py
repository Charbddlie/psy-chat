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

async def handle_info(data, user_id):
    required_fields = [
        "user_name", "age", "gender", "major", "grade", "aiAttitude", "time"
    ]
    missing = check_required_fields(data, required_fields)
    if missing:
        return {"type": "error", "msg": f"缺少字段: {missing}"}
    dir_name = f"{data['user_name']}_{user_id}"
    dir_path = os.path.join(LOG_DIR, dir_name)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, "info.json")
    # 为了防止有傻子做后测提交成前测然后覆盖info.json导致后测那边判断是刚刚做的时间不满七天不给做后测，所以这里就不覆盖存储了
    if os.path.exists(file_path):
        return {"type": "info_exist", "user_name": data['user_name']}
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"type": "info_success", "user_name": data['user_name']}

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
    return {"type": "post_questionnaire_success", "user_name": data['user_name']}

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
    return {"type": "pre_questionnaire_success", "user_name": data['user_name']}

async def handle_final_questionnaire(data, user_id):
    required_fields = [
        "user_name"
    ]
    missing = check_required_fields(data, required_fields)
    if missing:
        return {"type": "error", "msg": f"缺少字段: {missing}"}
    dir_name = f"{data['user_name']}_{user_id}"
    dir_path = os.path.join(LOG_DIR, dir_name)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, "final.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"type": "final_questionnaire_success", "user_name": data['user_name']}


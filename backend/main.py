import asyncio
# import aiohttp
import websockets
import json
import tomli
import os
import uuid
import time
from chat import LLMChat
from questionnaire import *
import random
import string
import logging
from datetime import datetime

# 存储所有活跃的chat实例，结构: {chat_id: {"instance": ..., "last_active": ...}}
chat_instances = {}

CHAT_INSTANCE_TIMEOUT = 600  # 单位: 秒

def update_chat_last_active(chat_id):
    if chat_id in chat_instances:
        chat_instances[chat_id]["last_active"] = time.time()

def get_record(remote_address, user_name, user_id):
    log_dir = tomli.load(open('settings.toml', 'rb'))["log_dir"]
    folder_path = os.path.join(log_dir, f"{user_name}_{user_id}")
    # 检查文件完成情况
    record = {
        "user_name": user_name,
        "user_id": user_id,
        "info": False,
        "pre": False,
        "post": False,
        "chat": False,
        "chat_complete": False,
        "excluded": False,
        "timestamp": 0
    }
    
    # 检查文件存在情况
    info_file = os.path.join(folder_path, "info.json")
    if os.path.isfile(info_file):
        record["info"] = True
        # 获取info.json的time作为时间戳
        try:
            with open(info_file, "r", encoding="utf-8") as f:
                info_data = json.load(f)
            time_str = info_data.get("time")
            # 处理 "2025-07-30 21:25:35" 这种类型的字符串
            if time_str:
                try:
                    dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                    record["timestamp"] = int(dt.timestamp())
                except Exception:
                    record["timestamp"] = 0
            else:
                record["timestamp"] = 0
        except Exception:
            record["timestamp"] = 0
        
    pre_file = os.path.join(folder_path, "pre.json")
    if os.path.isfile(pre_file):
        record["pre"] = True
        # 检查pre.json中的excluded是不是true，如果是，把所有字段都设置为True然后返回
        try:
            with open(pre_file, "r", encoding="utf-8") as f:
                pre_data = json.load(f)
            if pre_data.get("excluded", False) is True:
                record["excluded"] = True
        except Exception:
            logger.info(f"{remote_address} exec:session_query, pre.json file error")
        
    post_file = os.path.join(folder_path, "post.json")
    if os.path.isfile(post_file):
        record["post"] = True
    
    chat_file = os.path.join(folder_path, "chat.tsv")
    if os.path.isfile(chat_file):
        # 检查聊天是否完成
        try:
            with open(chat_file, "r", encoding="utf8") as f:
                lines = f.readlines()
            if len(lines) >= 2:
                record["chat"] = True
                last_line = lines[-1].rstrip("\n")
                header = lines[0].rstrip("\n").split("\t")
                last_fields = last_line.split("\t")
                if len(last_fields) == len(header):
                    role_idx = header.index("role") if "role" in header else None
                    text_idx = header.index("text") if "text" in header else None
                    if role_idx is not None and text_idx is not None:
                        if last_fields[role_idx] == "AI" and "聊天已结束" in last_fields[text_idx]:
                            record["chat_complete"] = True
        except Exception as e:
            logger.info(f"{remote_address} exec:session_query, chat file error")
    return record

async def cleanup_chat_instances():
    """定期清理超时未活跃的chat实例"""
    while True:
        now = time.time()
        to_delete = []
        for chat_id, info in list(chat_instances.items()):
            last_active = info.get("last_active", 0)
            if now - last_active > CHAT_INSTANCE_TIMEOUT:
                to_delete.append(chat_id)
        for chat_id in to_delete:
            logger.info(f"清理chat实例: chat_id:{chat_id}")
            del chat_instances[chat_id]
        await asyncio.sleep(60)  # 每分钟检查一次

async def chat(websocket, chat_instance, chat_id, user_message=""):
    try:
        # 先发送消息确认，让客户端知道消息已收到
        if user_message:
            logger.debug(f"{websocket.remote_address} recv:chat, chat_id:{chat_id} {user_message}")
            await websocket.send(json.dumps({"type": "chat_received"}))
            logger.debug(f"{websocket.remote_address} send:chat_received, chat_id:{chat_id} {user_message}")
        else:
            logger.debug(f"{websocket.remote_address} recv:chat, chat_id:{chat_id} prompt chat")
            
        # 处理聊天
        async for chunk in chat_instance.chat(user_message):
            await websocket.send(json.dumps({"type": "chat_chunk", "content": chunk}))
        ai_message = chat_instance.history[-1]["content"]
        await websocket.send(json.dumps({"type": "chat_chunk_end", "ai_message":ai_message}))
        logger.debug(f"{websocket.remote_address} send:chat_chunk_end, chat_id:{chat_id} ai_message:{ai_message}")
    except asyncio.TimeoutError:
        logger.warning(f"asyncio API请求超时")
        await websocket.send(json.dumps({"type": "chat_time_out"}))
    # except aiohttp.ClientError:
    #     logger.warning(f"aiohttp API请求超时")
    #     await websocket.send(json.dumps({"type": "chat_time_out"}))
    except Exception as e:
        logger.exception(f"API请求失败")
        await websocket.send(json.dumps({"type": "error", "content": f"API请求失败: {e}"}))

async def websocket_handler(websocket):
    """处理WebSocket连接的异步函数"""
    logger.info(f"{websocket.remote_address} 新的WebSocket连接")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                msg_type = data.get("type")
                logger.info(f"{websocket.remote_address} recv:{msg_type}")

                if msg_type == "ping":
                    await websocket.send(json.dumps({"type": "pong", "content": "服务器正常"}))
                    logger.info(f"{websocket.remote_address} send:pong")

                elif msg_type == "session_query":
                    # 根据用户名查询所有历史会话
                    search_name = data.get("search_name", "")
                    if not search_name:
                        await websocket.send(json.dumps({"type": "query_result", "records": []}))
                        logger.info(f"{websocket.remote_address} send:query_result, no search_name")
                        continue
                        
                    # 搜索log目录下所有包含此名字的文件夹
                    records = []
                    log_dir = tomli.load(open('settings.toml', 'rb'))["log_dir"]
                    
                    if not os.path.isdir(log_dir):
                        await websocket.send(json.dumps({"type": "query_result", "records": records}))
                        logger.info(f"{websocket.remote_address} send:query_result, search_name:{search_name}, no records")
                        continue
                        
                    for dirname in os.listdir(log_dir):
                        folder_path = os.path.join(log_dir, dirname)
                        if not os.path.isdir(folder_path): continue
                        # 解析目录名获取用户名和ID
                        parts = dirname.split("_")
                        if len(parts) < 2: continue
                        
                        user_name = "_".join(parts[:-1]) # 名称可能会包含_
                        if search_name != user_name:  continue
                        user_id = parts[-1]
                        
                        record = get_record(websocket.remote_address, user_name, user_id)
                        records.append(record)
                
                    # 按完成度和时间排序
                    records.sort(key=lambda x: (-sum([x["info"], x["pre"], x["post"], x["chat"]]), -x["timestamp"]))
                    
                    await websocket.send(json.dumps({"type": "query_result", "records": records}))
                    logger.info(f"{websocket.remote_address} send:query_result, search_name:{search_name}, records:{" and ".join([f"{i["user_name"]}_{i["user_id"]}" for i in records])}")
                
                elif msg_type == "chat_create":
                    # 如果还有chat_id
                    chat_id = data.get("chat_id")
                    user_id = data.get("user_id")
                    user_name = data.get("user_name", "defaultName")
                    
                    # 如果有user_id, 就是用户选择的，存在不存在都行
                    if not user_id:
                        # 生成16位随机user_id，确保目录不存在
                        log_dir = tomli.load(open('settings.toml', 'rb'))["log_dir"]
                        while True:
                            user_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                            folder_name = f"{user_name}_{user_id}"
                            folder_path = os.path.join(log_dir, folder_name)
                            if not os.path.exists(folder_path):
                                break
                        logger.info(f"{websocket.remote_address} exec:chat_create, user_name:{user_name}, create user_id:{user_id}")
                    if chat_id and chat_id in chat_instances and chat_instances[chat_id]["user_id"] == user_id and chat_instances[chat_id]["user_name"] == user_name:
                        chat_instance = chat_instances[chat_id]["instance"]
                        update_chat_last_active(chat_id)
                        logger.info(f"{websocket.remote_address} exec:chat_create, 再访问chat实例:{user_name}_{user_id} chat_id:{chat_id}")
                    else:
                        # 没有chat_id或chat_id已失效
                        chat_id = str(uuid.uuid4())
                        chat_instance = LLMChat(user_name, user_id)
                        
                        chat_instances[chat_id] = {
                            "instance": chat_instance,
                            "last_active": time.time(),
                            "user_name": user_name,
                            "user_id": user_id,
                        }
                        logger.info(f"{websocket.remote_address} exec:chat_create, 创建新chat实例:{user_name}_{user_id} chat_id:{chat_id}")
                    
                    record = get_record(websocket.remote_address, user_name, user_id)
                    # chat_history = chat_instance.get_history()
                    await websocket.send(json.dumps({"type": "chat_created", "chat_id": chat_id, 'record': record}))
                    logger.info(f"{websocket.remote_address} send:chat_created, chat_id:{chat_id}, {user_name}_{user_id}")
                    # await websocket.send(json.dumps({"type": "chat_created", "chat_id": chat_id, "chat_history": chat_history, 'record': record}))
                    # logger.debug(f"{websocket.remote_address} send:chat_created, chat_id:{chat_id}, {user_name}_{user_id} chat_id:{chat_id}, chat_history_len:{len(chat_history)}")
                    # await chat(websocket, chat_instance, chat_id)
                elif msg_type == "chat_history":
                    chat_id = data.get("chat_id")
                    if not chat_id or chat_id not in chat_instances:
                        await websocket.send(json.dumps({"type": "error", "content": f"无效的chat_id:{chat_id}"}))
                        logger.info(f"{websocket.remote_address} send:error, content:{f'无效的chat_id:{chat_id}'}")
                        continue
                    update_chat_last_active(chat_id)
                    chat_instance = chat_instances[chat_id]["instance"]
                    chat_history = chat_instance.get_history()
                    await websocket.send(json.dumps({"type": "chat_history", "chat_history": chat_history}))
                    user_name = chat_instances[chat_id]['user_name']
                    user_id = chat_instances[chat_id]['user_id']
                    logger.info(f"{websocket.remote_address} send:chat_history, chat_id:{chat_id}, {user_name}_{user_id}, chat_history_len:{len(chat_history)}")
                elif msg_type == "chat":
                    chat_id = data.get("chat_id")
                    if not chat_id or chat_id not in chat_instances:
                        await websocket.send(json.dumps({"type": "error", "content": f"无效的chat_id:{chat_id}"}))
                        logger.info(f"{websocket.remote_address} send:error, content:{f'无效的chat_id:{chat_id}'}")
                        continue
                    update_chat_last_active(chat_id)
                    chat_instance = chat_instances[chat_id]["instance"]
                    await chat(websocket, chat_instance, chat_id, data.get("content"))
                elif msg_type == "chat_end":
                    chat_id = data.get("chat_id")
                    if not chat_id or chat_id not in chat_instances:
                        await websocket.send(json.dumps({"type": "error", "content": f"无效的chat_id:{chat_id}"}))
                        logger.info(f"{websocket.remote_address} send:error, content:{f'无效的chat_id:{chat_id}'}")
                        continue
                    update_chat_last_active(chat_id)
                    await websocket.send(json.dumps({"type": "chat_ended", "chat_id": chat_id}))
                    logger.info(f"{websocket.remote_address} send:chat_ended, chat_id:{chat_id}")

                elif msg_type == "info_collect":
                    user_id = data.get("user_id")
                    result = await handle_info(data.get("data", {}), user_id)
                    await websocket.send(json.dumps(result))
                    logger.info(f"{websocket.remote_address} send:info_collect, {result}")
                elif msg_type == "pre_questionnaire":
                    user_id = data.get("user_id")
                    result = await handle_pre_questionnaire(data.get("data", {}), user_id)
                    await websocket.send(json.dumps(result))
                    logger.info(f"{websocket.remote_address} send:pre_questionnaire, {result}")
                elif msg_type == "post_questionnaire":
                    user_id = data.get("user_id")
                    result = await handle_post_questionnaire(data.get("data", {}), user_id)
                    await websocket.send(json.dumps(result))
                    logger.info(f"{websocket.remote_address} send:post_questionnaire, {result}")
                elif msg_type == "final_questionnaire":
                    user_id = data.get("user_id")
                    result = await handle_final_questionnaire(data.get("data", {}), user_id)
                    await websocket.send(json.dumps(result))
                    logger.info(f"{websocket.remote_address} send:final_questionnaire, {result}")
                else:
                    await websocket.send(json.dumps({"type": "info", "content": "已收到消息"}))
                    logger.info(f"{websocket.remote_address} send:info, {'已收到消息'}")
            except json.JSONDecodeError:
                await websocket.send(json.dumps({"type": "error", "content": "无效的JSON格式"}))
                logger.exception(f"{websocket.remote_address} exec:无效的JSON格式")
            except Exception as e:
                await websocket.send(json.dumps({"type": "error", "content": str(e)}))
                logger.exception(f"{websocket.remote_address}")
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"{websocket.remote_address} websocket连接已关闭")
    except Exception as e:
        await websocket.send(json.dumps({"type": "error", "content": str(e)}))
        logger.exception(f"{websocket.remote_address} websocket出错")

async def start_websocket_server():
    """启动WebSocket服务器"""
    settings = tomli.load(open('settings.toml', 'rb'))
    # 设置host为"0.0.0.0"以支持局域网所有设备连接
    host = settings.get('websocket_host', '0.0.0.0')
    port = settings.get('websocket_port', 8765)

    logger.info(f"启动WebSocket服务器: ws://{host}:{port}")
    # 启动定时清理任务
    loop = asyncio.get_running_loop()
    loop.create_task(cleanup_chat_instances())
    server = await websockets.serve(websocket_handler, host, port)
    logger.info(f"WebSocket服务器已启动, 等待连接...")
    await server.wait_closed()

if __name__ == "__main__":
    # 创建日志目录
    log_dir = "log/runlog"
    os.makedirs(log_dir, exist_ok=True)
    log_filename = datetime.now().strftime("%Y%m%d-%H%M%S") + ".log"
    log_path = os.path.join(log_dir, log_filename)

    # 定义日志格式
    log_format = "[%(asctime)s] [%(levelname)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # 配置logger
    logger = logging.getLogger("main")
    logger.setLevel(logging.INFO)

    # 文件Handler
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))

    # 控制台Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))

    # 添加Handler
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    if LLMChat.chat_test:
        logger.info(f"chat test已启动, 聊天会模拟ai回复而不会实际调用ai服务")
    logger.info(f"日志已启动，写入:{log_path}")

    asyncio.run(start_websocket_server())
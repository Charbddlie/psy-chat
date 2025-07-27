import asyncio
import aiohttp
import websockets
import json
import tomli
import os
import uuid
import time
from chat import LLMChatFactory
from questionnaire import *

# 存储所有活跃的chat实例，结构: {chat_id: {"instance": ..., "last_active": ...}}
chat_instances = {}

CHAT_INSTANCE_TIMEOUT = 600  # 10分钟，单位: 秒

def update_chat_last_active(chat_id):
    if chat_id in chat_instances:
        chat_instances[chat_id]["last_active"] = time.time()

async def cleanup_chat_instances():
    """定期清理10分钟未活跃的chat实例"""
    while True:
        now = time.time()
        to_delete = []
        for chat_id, info in list(chat_instances.items()):
            last_active = info.get("last_active", 0)
            if now - last_active > CHAT_INSTANCE_TIMEOUT:
                to_delete.append(chat_id)
        for chat_id in to_delete:
            print(f"清理chat实例: chat_id={chat_id}")
            del chat_instances[chat_id]
        await asyncio.sleep(60)  # 每分钟检查一次

async def chat(websocket, chat_instance, chat_id, user_message=""):
    try:
        if user_message: print(f"发送聊天消息：{user_message}")
        async for chunk in chat_instance.chat(user_message):
            await websocket.send(json.dumps({"type": "chat_chunk", "content": chunk}))
        await websocket.send(json.dumps({"type": "chat_chunk_end"}))
        update_chat_last_active(chat_id)
    except asyncio.TimeoutError:
        await websocket.send(json.dumps({"type": "chat_time_out"}))
        print(f"API请求超时")
    except aiohttp.ClientError:
        print(f"API请求超时")
        await websocket.send(json.dumps({"type": "chat_time_out"}))
    except Exception as e:
        print(f"API请求失败: {e}")
        await websocket.send(json.dumps({"type": "error", "content": f"API请求失败: {e}"}))

async def chat_create(websocket, sample_name, sample_id):
    chat_id = str(uuid.uuid4())
    chat_instance = LLMChatFactory.create_llm_chat(sample_name, sample_id)
    chat_instances[chat_id] = {
        "instance": chat_instance,
        "last_active": time.time()
    }
    print(f"创建新chat实例: chat_id={chat_id}, {chat_instance}")
    await websocket.send(json.dumps({"type": "chat_created", "chat_id": chat_id}))
    await chat(websocket, chat_instance, chat_id)

async def websocket_handler(websocket):
    """处理WebSocket连接的异步函数"""
    print(f"新的WebSocket连接: {websocket.remote_address}")
    chat_id = None
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                msg_type = data.get("type")
                print(f"收到消息: {msg_type}")

                if msg_type == "ping":
                    await websocket.send(json.dumps({"type": "pong", "content": "服务器正常"}))
                elif msg_type == "chat_create":
                    # 客户端请求创建新会话，参数在data中
                    sample_name = data.get("sample_name", "default_name")
                    sample_id = data.get("sample_id", "default_id")
                    await chat_create(websocket, sample_name, sample_id)

                elif msg_type == "chat_continue":
                    # 把用户的所有聊天记录全部发送过去，包括最后一次用户的输入（如果存在），让用户重新发送聊天请求
                    chat_id = data.get("chat_id")
                    if chat_id and chat_id in chat_instances:
                        chat_instance = chat_instances[chat_id]["instance"]
                        chat_history = chat_instance.get_history()
                        if len(chat_history) > 0:
                            await websocket.send(json.dumps({"type": "chat_continued","chat_id": chat_id, "chat_history": chat_history}))
                            continue
                    
                    # 客户端请求创建新会话，参数在data中
                    sample_name = data.get("sample_name", "default_name")
                    sample_id = data.get("sample_id", "default_id")
                    await chat_create(websocket, sample_name, sample_id)
                elif msg_type == "chat":
                    chat_id = data.get("chat_id")
                    if not chat_id or chat_id not in chat_instances:
                        await websocket.send(json.dumps({"type": "error", "content": f"无效的chat_id:{chat_id}"}))
                        continue
                    chat_instance = chat_instances[chat_id]["instance"]
                    await chat(websocket, chat_instance, chat_id, data.get("content"))

                elif msg_type == "info_collect":
                    result = await handle_submit(data.get("data", {}))
                    print(f"发送消息：{result}")
                    await websocket.send(json.dumps(result))
                elif msg_type == "pre_questionnaire":
                    result = await handle_pre_questionnaire(data.get("data", {}))
                    print(f"发送消息：{result}")
                    await websocket.send(json.dumps(result))
                elif msg_type == "post_questionnaire":
                    result = await handle_post_questionnaire(data.get("data", {}))
                    print(f"发送消息：{result}")
                    await websocket.send(json.dumps(result))
                else:
                    await websocket.send(json.dumps({"type": "info", "content": "已收到消息"}))
            except json.JSONDecodeError:
                print(f"无效的JSON格式")
                await websocket.send(json.dumps({"type": "error", "content": "无效的JSON格式"}))
            except Exception as e:
                print(f"处理消息时出错: {e}")
                await websocket.send(json.dumps({"type": "error", "content": str(e)}))
    except websockets.exceptions.ConnectionClosed:
        print(f"WebSocket连接已关闭: {websocket.remote_address}")
    except Exception as e:
        print(f"WebSocket服务器错误: {e}")
        await websocket.send(json.dumps({"type": "error", "content": str(e)}))

async def start_websocket_server():
    """启动WebSocket服务器"""
    settings = tomli.load(open('settings.toml', 'rb'))
    # 设置host为"0.0.0.0"以支持局域网所有设备连接
    host = settings.get('websocket_host', '0.0.0.0')
    port = settings.get('websocket_port', 8765)

    print(f"启动WebSocket服务器: ws://{host}:{port}")
    # 启动定时清理任务
    loop = asyncio.get_running_loop()
    loop.create_task(cleanup_chat_instances())
    server = await websockets.serve(websocket_handler, host, port)
    print(f"WebSocket服务器已启动，等待连接...")
    await server.wait_closed()

if __name__ == "__main__":
    print("聊天会话已准备就绪，启动WebSocket服务器...")
    asyncio.run(start_websocket_server())
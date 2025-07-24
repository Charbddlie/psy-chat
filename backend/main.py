import asyncio
import websockets
import json
import tomli
import os
import uuid
from chat import LLMChatFactory
from questionnaire import *

# 存储所有活跃的chat实例
chat_instances = {}

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
                elif msg_type == "create":
                    # 客户端请求创建新会话，参数在data中
                    sample_name = data.get("sample_name", "default_name")
                    sample_id = data.get("sample_id", "default_id")
                    chat_id = str(uuid.uuid4())
                    chat_instance = LLMChatFactory.create_llm_chat(sample_name, sample_id)
                    chat_instances[chat_id] = chat_instance
                    print(f"创建新chat实例: chat_id={chat_id}, {chat_instance}")
                    await websocket.send(json.dumps({"type": "created", "chat_id": chat_id}))
                    json_message = chat_instance.chat()
                    await websocket.send(json_message)
                elif msg_type == "chat":
                    chat_id = data.get("chat_id")
                    if not chat_id or chat_id not in chat_instances:
                        await websocket.send(json.dumps({"type": "error", "content": "无效的chat_id"}))
                        continue
                    chat_instance = chat_instances[chat_id]
                    json_message = chat_instance.chat(data.get("content"))
                    await websocket.send(json_message)
                elif msg_type == "info_collect":
                    result = await handle_submit(data.get("data", {}))
                    print(f"发送消息：{result['type']}")
                    await websocket.send(json.dumps(result))
                elif msg_type == "pre_questionnaire":
                    result = await handle_pre_questionnaire(data.get("data", {}))
                    print(f"发送消息：{result['type']}")
                    await websocket.send(json.dumps(result))
                elif msg_type == "post_questionnaire":
                    result = await handle_post_questionnaire(data.get("data", {}))
                    print(f"发送消息：{result['type']}")
                    await websocket.send(json.dumps(result))
                else:
                    await websocket.send(json.dumps({"type": "info", "content": "已收到消息"}))
            except json.JSONDecodeError:
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
    server = await websockets.serve(websocket_handler, host, port)
    print(f"WebSocket服务器已启动，等待连接...")
    await server.wait_closed()

if __name__ == "__main__":
    print("聊天会话已准备就绪，启动WebSocket服务器...")
    asyncio.run(start_websocket_server())
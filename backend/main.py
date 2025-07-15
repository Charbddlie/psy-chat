import asyncio
import websockets
import json
import tomli
import os
import uuid
from chat import LLMChatFactory, csv_filename

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
                print(f"收到消息: {data}")

                msg_type = data.get("type")
                if msg_type == "ping":
                    await websocket.send(json.dumps({"type": "pong", "content": "服务器正常"}))
                elif msg_type == "create":
                    # 客户端请求创建新会话，参数在data中
                    topic = data.get("topic", "thunder")
                    sociability = data.get("sociability", "high")
                    initiativity = data.get("initiativity", "low")
                    chat_id = str(uuid.uuid4())
                    chat_instance = LLMChatFactory.create_llm_chat(
                        topic=topic,
                        sociability=sociability,
                        initiativity=initiativity
                    )
                    chat_instances[chat_id] = chat_instance
                    print(f"创建新chat实例: chat_id={chat_id}, {chat_instance}")
                    await websocket.send(json.dumps({"type": "created", "chat_id": chat_id}))
                    json_message = chat_instance.chat(data.get("content"))
                    await websocket.send(json_message)
                elif msg_type == "chat":
                    chat_id = data.get("chat_id")
                    if not chat_id or chat_id not in chat_instances:
                        await websocket.send(json.dumps({"type": "error", "content": "无效的chat_id"}))
                        continue
                    chat_instance = chat_instances[chat_id]
                    json_message = chat_instance.chat(data.get("content"))
                    await websocket.send(json_message)
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
    host = settings.get('websocket_host', 'localhost')
    port = settings.get('websocket_port', 8765)

    print(f"启动WebSocket服务器: ws://{host}:{port}")
    server = await websockets.serve(websocket_handler, host, port)
    print(f"WebSocket服务器已启动，等待连接...")
    await server.wait_closed()

if __name__ == "__main__":
    print("聊天会话已准备就绪，启动WebSocket服务器...")
    asyncio.run(start_websocket_server())
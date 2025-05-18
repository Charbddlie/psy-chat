import argparse
from datetime import datetime
from chat import LLMChatFactory, csv_filename
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PsyChat LLM 配置文件")
    parser.add_argument("--topic", type=str, default="thunder", help="LLM 聊天的主题 (例如: thunder)")
    parser.add_argument("--sociability", type=str, default="high", choices=['high', 'low'], help="LLM 聊天的社交性级别 (high/low)")
    parser.add_argument("--initiativity", type=str, default="low", choices=['high', 'low'], help="LLM 聊天的启动性级别 (high/low)")

    args = parser.parse_args()

    print(f"接收到的参数: Topic={args.topic}, Sociability={args.sociability}, Initiativity={args.initiativity}")
    
    llm_chat_instance = LLMChatFactory.create_llm_chat(
        topic=args.topic,
        sociability=args.sociability,
        initiativity=args.initiativity
    )
    print(f"LLM Chat 实例创建成功: {llm_chat_instance}")

    # llm_chat_instance.start_chat_session()
    
    # 添加WebSocket服务器功能
    import asyncio
    import websockets
    import json
    import tomli
    import os
    
    async def websocket_handler(websocket):
        """处理WebSocket连接的异步函数"""
        print(f"新的WebSocket连接: {websocket.remote_address}")
        try:
            # 处理来自客户端的消息
            async for message in websocket:
                try:
                    data = json.loads(message)
                    print(f"收到消息: {data}")
                    
                    # 根据消息类型处理
                    if data.get("type") == "ping":
                        # 处理心跳检测
                        await websocket.send(json.dumps({"type": "pong", "content": "服务器正常"}))
                    elif data.get("type") == "chat":
                        json_message = llm_chat_instance.chat(data.get("content"))
                        await websocket.send(json_message)
                    elif data.get("type") == "start":
                        json_message = llm_chat_instance.chat_start()
                        await websocket.send(json_message)
                    else:
                        # 其他类型的消息
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
        # 从配置文件读取设置
        settings = tomli.load(open('settings.toml', 'rb'))
        host = settings.get('websocket_host', 'localhost')
        port = settings.get('websocket_port', 8765)
        
        print(f"启动WebSocket服务器: ws://{host}:{port}")
        server = await websockets.serve(websocket_handler, host, port)
        print(f"WebSocket服务器已启动，等待连接...")
        await server.wait_closed()
    
    # 在主程序结束后启动WebSocket服务器
    print("聊天会话已准备就绪，启动WebSocket服务器...")
    asyncio.run(start_websocket_server())
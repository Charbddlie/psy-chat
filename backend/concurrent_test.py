import asyncio
import websockets
import json
import time
import random
import uuid
from datetime import datetime
import argparse

# 配置参数
parser = argparse.ArgumentParser(description='测试WebSocket服务器的并发能力')
parser.add_argument('--connections', '-c', type=int, default=100, help='并发连接数 (默认: 100)')
parser.add_argument('--host', type=str, default='localhost', help='WebSocket服务器地址 (默认: localhost)')
parser.add_argument('--port', type=int, default=8765, help='WebSocket服务器端口 (默认: 8765)')
parser.add_argument('--wait', type=float, default=2.0, help='所有连接建立后等待多少秒再统一发起测试 (默认: 2.0)')
args = parser.parse_args()

# 统计数据
total_connections = args.connections
successful_first_responses = 0
successful_complete_responses = 0
connection_errors = 0
response_times = []
complete_response_times = []

# 随机名字列表，用于测试
test_names = [
    "压力测试"
]

# 用于同步所有连接建立
all_connected_event = asyncio.Event()
connected_count = 0
connected_count_lock = asyncio.Lock()

# 全局统一开始时间戳
start_timestamp = time.time() + 3600  # 先设为很大，后面动态调整
start_timestamp_lock = asyncio.Lock()

async def test_chat_session(session_id):
    """测试单个聊天会话，等待统一开始时间"""
    global successful_first_responses, successful_complete_responses, connection_errors, connected_count, start_timestamp

    ws_url = f"ws://{args.host}:{args.port}"

    try:
        # 生成测试用户信息
        test_name = random.choice(test_names) + str(session_id)

        print(f"[{session_id}] 开始连接: {test_name}")

        # 连接WebSocket
        async with websockets.connect(ws_url) as websocket:
            # 连接建立后，计数
            async with connected_count_lock:
                connected_count += 1
                if connected_count == total_connections:
                    all_connected_event.set()

            # 等待所有连接建立
            await all_connected_event.wait()

            # 等待到统一的开始时间戳
            while True:
                async with start_timestamp_lock:
                    current_start_timestamp = start_timestamp
                now = time.time()
                wait_time = current_start_timestamp - now
                if wait_time <= 0:
                    break
                await asyncio.sleep(min(wait_time, 0.05))

            # 创建聊天会话
            await websocket.send(json.dumps({
                "type": "chat_create",
                "user_name": test_name,
            }))

            # 等待会话创建确认
            response = await websocket.recv()
            data = json.loads(response)

            if data["type"] != "chat_created":
                print(f"[{session_id}] 会话创建失败: {data}")
                return

            chat_id = data["type"] == "chat_created" and data.get("chat_id")
            if not chat_id:
                print(f"[{session_id}] 无法获取chat_id")
                return

            # 接收AI的初始回复
            first_message_start = None
            first_response_received = False
            complete_message_received = False
            start_time = time.time()

            # 等待初始消息并记录时间
            while True:
                response = await websocket.recv()
                data = json.loads(response)

                if data["type"] == "chat_chunk" and not first_response_received:
                    first_message_start = time.time()
                    time_to_first = first_message_start - start_time
                    response_times.append(time_to_first)
                    print(f"[{session_id}] 首次响应时间: {time_to_first:.2f}秒")
                    first_response_received = True
                    successful_first_responses += 1

                if data["type"] == "chat_chunk_end":
                    complete_time = time.time() - start_time
                    complete_response_times.append(complete_time)
                    print(f"[{session_id}] 完整响应时间: {complete_time:.2f}秒")
                    successful_complete_responses += 1
                    complete_message_received = True
                    break

                # 超时保护
                if time.time() - start_time > 30:
                    print(f"[{session_id}] 响应超时")
                    break

            # 发送测试消息
            if complete_message_received:
                test_message = "这是一个并发测试消息"
                await websocket.send(json.dumps({
                    "type": "chat",
                    "chat_id": chat_id,
                    "content": test_message
                }))

                # 等待确认
                message_confirmed = False
                chunks_received = False
                message_completed = False
                message_start_time = time.time()

                while True:
                    response = await websocket.recv()
                    data = json.loads(response)

                    if data["type"] == "chat_received":
                        message_confirmed = True
                        print(f"[{session_id}] 消息确认时间: {time.time() - message_start_time:.2f}秒")

                    if data["type"] == "chat_chunk" and not chunks_received:
                        chunks_received = True
                        message_response_time = time.time() - message_start_time
                        print(f"[{session_id}] 消息首次响应时间: {message_response_time:.2f}秒")

                    if data["type"] == "chat_chunk_end":
                        message_completed = True
                        message_complete_time = time.time() - message_start_time
                        print(f"[{session_id}] 消息完整响应时间: {message_complete_time:.2f}秒")
                        break

                    # 超时保护
                    if time.time() - message_start_time > 30:
                        print(f"[{session_id}] 消息响应超时")
                        break

                # 结束会话
                await websocket.send(json.dumps({
                    "type": "chat_end",
                    "chat_id": chat_id
                }))

                # 等待会话结束确认
                response = await websocket.recv()
                data = json.loads(response)
                if data["type"] == "chat_ended":
                    print(f"[{session_id}] 会话已正常结束")

    except Exception as e:
        print(f"[{session_id}] 错误: {e}")
        connection_errors += 1

    print(f"[{session_id}] 测试完成")

async def run_test():
    """运行并发测试，所有连接建立后统一开始"""
    global start_timestamp
    print(f"开始测试 {total_connections} 个并发连接 to ws://{args.host}:{args.port}")

    # 统一的开始时间戳（所有连接建立后再延迟args.wait秒）
    async def prepare_and_run():
        global start_timestamp
        # 先让所有连接协程准备好
        tasks = [asyncio.create_task(test_chat_session(i)) for i in range(total_connections)]

        # 等待所有连接建立
        while True:
            await asyncio.sleep(0.05)
            if all_connected_event.is_set():
                break

        # 统一设置开始时间
        async with start_timestamp_lock:
            start_timestamp = time.time() + args.wait
            print(f"所有连接已建立，{args.wait:.2f}秒后统一开始测试 ({datetime.fromtimestamp(start_timestamp).strftime('%H:%M:%S.%f')})")

        # 等待所有任务完成
        await asyncio.gather(*tasks)

    start_time = time.time()
    await prepare_and_run()

    # 计算统计结果
    test_duration = time.time() - start_time
    success_rate_first = (successful_first_responses / total_connections) * 100
    success_rate_complete = (successful_complete_responses / total_connections) * 100

    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    avg_complete_time = sum(complete_response_times) / len(complete_response_times) if complete_response_times else 0

    # 计算百分位数
    percentiles = {}
    if response_times:
        response_times.sort()
        percentiles["50th_percentile"] = response_times[int(len(response_times) * 0.5)]
        percentiles["90th_percentile"] = response_times[int(len(response_times) * 0.9)]
        percentiles["95th_percentile"] = response_times[int(len(response_times) * 0.95)]
        percentiles["99th_percentile"] = response_times[int(len(response_times) * 0.99)]

    # 输出结果
    print("\n" + "=" * 50)
    print(f"并发测试结果 ({total_connections} 连接):")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总测试时长: {test_duration:.2f} 秒")
    print("-" * 50)
    print(f"连接成功率: {((total_connections - connection_errors) / total_connections) * 100:.1f}% ({total_connections - connection_errors}/{total_connections})")
    print(f"10秒内首次响应成功率: {success_rate_first:.1f}% ({successful_first_responses}/{total_connections})")
    print(f"15秒内完成响应成功率: {success_rate_complete:.1f}% ({successful_complete_responses}/{total_connections})")
    print("-" * 50)
    print(f"平均首次响应时间: {avg_response_time:.2f} 秒")
    print(f"平均完成响应时间: {avg_complete_time:.2f} 秒")

    if percentiles:
        print("-" * 50)
        print("响应时间分布:")
        print(f"50% 的请求在 {percentiles['50th_percentile']:.2f} 秒内获得首次响应")
        print(f"90% 的请求在 {percentiles['90th_percentile']:.2f} 秒内获得首次响应")
        print(f"95% 的请求在 {percentiles['95th_percentile']:.2f} 秒内获得首次响应")
        print(f"99% 的请求在 {percentiles['99th_percentile']:.2f} 秒内获得首次响应")

    print("=" * 50)

    # 输出结果判断
    if success_rate_first >= 90 and success_rate_complete >= 85:
        print("✅ 测试通过: 服务器性能良好")
    elif success_rate_first >= 70 and success_rate_complete >= 65:
        print("⚠️ 测试结果不理想: 服务器性能可能需要优化")
    else:
        print("❌ 测试失败: 服务器性能不佳，需要调查问题")

if __name__ == "__main__":
    # 运行测试
    asyncio.run(run_test())
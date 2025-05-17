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

    llm_chat_instance.start_chat_session()
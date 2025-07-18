from action import *
import os
from dataclasses import dataclass
from datetime import datetime
import tomli
import json
import asyncio
import websockets
import json
import tomli
import os

import openai

log_dir = tomli.load(open('settings.toml', 'rb'))['log_dir']
# tsv_filename = None
last_time = None
def log(role, text, log_path):
    global last_time
    os.makedirs(log_dir, exist_ok=True)
    time = datetime.now()
    if not last_time: last_time = time
    resp_time = f"{(time - last_time).total_seconds():.2f}"
    # 创建新记录
    record_data = {
        'role': role,
        'text_len': str(len(text)),
        'resp_time': str(resp_time),
        'time': str(time),
        'text': text.replace('\n', '\\n'),
    }
    # for k,v in record_data.items():
    #     print(f"{k}: {v}")
    record_data = {k: v.strip().replace('\t','    ') for k,v in record_data.items()}
    # 保存到tsv文件
    if not os.path.exists(log_path):
        with open(log_path, 'w', encoding='utf8') as f:
            f.write('\t'.join(record_data.keys()) + '\n')
        
    with open(log_path, 'a', encoding='utf8') as f:
        f.write('\t'.join(record_data.values()) + '\n')

class LLM_Chat():
    def __init__(self, sample_name, sample_id):
        # self.chat_dict = {}
        self.sample_name = sample_name
        self.sample_id = sample_id
        settings = tomli.load(open('settings.toml', 'rb'))
        log_dir = settings['log_dir']
        self.log_path = f'{log_dir}/{self.sample_name}_{sample_id}.tsv'
        with open('thunder_prompt.txt', 'r', encoding='utf8') as f:
            self.prompt = f.read()
        # 支持自定义 API key 和 base url
        openai.api_key = settings['api_key']
        openai.base_url = settings['base_url']

        self.model_name = settings['model_name'] if 'model_name' in settings else 'o4-mini'
        self.start_time = datetime.now()


    def chat(self, message=None):
        # 初始化对话历史
        if not hasattr(self, 'history'):
            self.history = []
            self.history.append({"role": "user", "content": self.prompt})

        # 如果有用户输入，加入历史
        elif message != None:
            # 在message后加上json格式的{time_spent: xx minutes}
            from datetime import datetime
            now = datetime.now()
            if hasattr(self, 'start_time'):
                time_spent = (now - self.start_time).total_seconds() // 60
            else:
                self.start_time = now
                time_spent = 0
            # 拼接message和time_spent信息
            message_with_time = f"{message}\n{{\"time_spent\": {int(time_spent)} minutes}}"
            self.history.append({"role": "user", "content": message_with_time})
            log("user", message_with_time, self.log_path)

        # 流式传输
        try:
            stream = openai.chat.completions.create(
                model=self.model_name,
                messages=self.history,
                stream=True,
            )
            ai_message = ""
            for chunk in stream:
                if not chunk.choices: continue
                delta = getattr(chunk.choices[0].delta, "content", None)
                if delta:
                    ai_message += delta
                    # 实时返回流式内容（可选：如需逐步推送到前端，可yield或通过websocket分片发送）
                    # 这里只拼接，最终整体返回
            if not ai_message:
                raise ValueError("API未返回有效内容")
        except Exception as e:
            return json.dumps({"type": "error", "content": f"API请求失败: {e}"})

        # 记录AI回复到历史
        self.history.append({"role": "assistant", "content": ai_message})

        # 日志记录
        log("AI", ai_message, self.log_path)

        # 返回给前端
        return json.dumps({"type": "chat", "content": ai_message})

    def __str__(self):
        return f'{self.log_path}'

class LLMChatFactory:
    """LLM聊天工厂类"""
    @staticmethod
    def create_llm_chat(sample_name, sample_id) -> LLM_Chat:
        """
        创建LLM聊天实例的工厂方法
        
        Returns:
            LLM_Chat实例
        """
        return LLM_Chat(sample_name, sample_id)
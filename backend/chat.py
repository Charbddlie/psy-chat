import os
from dataclasses import dataclass
from datetime import datetime
import tomli
import asyncio
import openai
import re
import aiohttp

log_dir = tomli.load(open('settings.toml', 'rb'))['log_dir']

def generate_log_record(role, text, time):
    """生成一条符合格式的日志记录（dict）"""
    record_data = {
        'role': role,
        'text_len': str(len(text)),
        'time': str(time),
        'text': text.replace('\n', '\\n'),
    }
    # 清理制表符
    record_data = {k: v.strip().replace('\t', '    ') for k, v in record_data.items()}
    return record_data

class LLM_Chat():
    def __init__(self, sample_name, sample_id):
        self.sample_name = sample_name
        self.sample_id = sample_id
        settings = tomli.load(open('settings.toml', 'rb'))
        self.log_dir = f"{settings['log_dir']}/{sample_name}_{sample_id}"
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_path = os.path.join(self.log_dir, "chat.tsv")
        with open('prompt/thunder_prompt.txt', 'r', encoding='utf8') as f:
            self.prompt = f.read().replace('{name}', sample_name)
        # 支持自定义 API key 和 base url
        openai.api_key = settings['api_key']
        openai.base_url = settings['base_url']

        self.model_name = settings['model_name'] if 'model_name' in settings else 'o4-mini'
        self.mock_cnt = 0

        self.log_records = []  # 存储所有日志记录（dict）
        # self.start_time = datetime.now()
        # self.last_time = None  # 用于计算resp_time

        self.log_saved = False

    async def chat(self, message=None):
        # 初始化对话历史
        if not hasattr(self, 'history'):
            self.history = []
            self.history.append({"role": "user", "content": self.prompt})
        # 如果有用户输入，加入历史
        elif message is not None:
            # now = datetime.now()
            # if hasattr(self, 'start_time'):
            #     time_spent = (now - self.start_time).total_seconds() // 60
            # else:
            #     self.start_time = now
            #     time_spent = 0
            # message_with_time = f"{message}\n{{\"time_spent\": {int(time_spent)} minutes}}"
            message_with_time = f"{message}"
            self.history.append({"role": "user", "content": message_with_time})

            # # 生成日志记录
            log_time = datetime.now()
            # if self.last_time is None:
            #     self.last_time = log_time
            # resp_time = f"{(log_time - self.last_time).total_seconds():.2f}"
            # record = generate_log_record("user", message_with_time, resp_time, log_time)
            # self.last_time = log_time
            
            record = generate_log_record("user", message_with_time, log_time)
            self.log_records.append(record)
        
        next_idx = len(self.history)
        # Set up timeout for the API call
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10.0)) as session:
            stream = openai.chat.completions.create(
                model=self.model_name,
                messages=self.history,
                stream=True,
                # Pass session to OpenAI client if needed (depends on OpenAI SDK version)
            )
            ai_message = ""
            for chunk in stream:
                if not chunk.choices:
                    continue
                delta = getattr(chunk.choices[0].delta, "content", None)
                if delta:
                    ai_message += delta
                    yield delta
            if not ai_message:
                raise ValueError("API未返回有效内容")


        # self.mock_cnt += 1
        # if self.mock_cnt >= 3: ai_message = "聊天已结束"
        # else: ai_message = "长"*300

        # 证明这是一个过时的回复，已经有新的回复了，这里可能有并发问题，但是这个场景不考虑
        if next_idx != len(self.history): return
        # 记录AI回复到历史
        self.history.append({"role": "assistant", "content": ai_message})

        # 生成AI日志记录
        log_time = datetime.now()
        # if self.last_time is None:
        #     self.last_time = log_time
        # resp_time = f"{(log_time - self.last_time).total_seconds():.2f}"
        # record = generate_log_record("AI", ai_message, resp_time, log_time)
        # self.last_time = log_time
        record = generate_log_record("AI", ai_message, log_time)
        self.log_records.append(record)
        
        # 删除chat instance是客户端发起的请求，但是为了防止收不到请求，在消息生成时就直接记录log了
        if "聊天已结束" in ai_message: self.save_log()

    def get_history(self):
        # 跳过第一条
        result = []
        for item in self.history[1:]:
            new_item = item.copy()
            # if "content" in new_item:
            #     new_item["content"] = re.sub(r'\n\{"time_spent": \d+ minutes\}$', '', new_item["content"])
            result.append(new_item)
        return result

    def save_log(self):
        """
        聊天结束时调用，将log_records存储到chat.tsv（如有重复则chat_1.tsv, chat_2.tsv...）
        """
        if self.log_saved: return
        self.log_saved = True
        # 生成唯一文件名
        base_path = os.path.join(self.log_dir, "chat.tsv")
        log_path = base_path
        idx = 1
        while os.path.exists(log_path):
            log_path = os.path.join(self.log_dir, f"chat_{idx}.tsv")
            idx += 1

        # 写入文件
        if self.log_records:
            with open(log_path, 'w', encoding='utf8') as f:
                # 写表头
                header = list(self.log_records[0].keys())
                f.write('\t'.join(header) + '\n')
                for record in self.log_records:
                    f.write('\t'.join(record.get(k, "") for k in header) + '\n')

    def __str__(self):
        return f'{self.log_path}'
    
    def __del__(self):
        self.save_log()

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
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
    def __init__(self, sample_name):
        # self.chat_dict = {}
        self.sample_name = sample_name
        settings = tomli.load(open('settings.toml', 'rb'))
        log_dir = settings['log_dir']
        self.log_path = f'{log_dir}/{self.sample_name}_{datetime.now().strftime("%Y%m%d-%H%M%S")}.tsv'
        with open('thunder_prompt.txt', 'r', encoding='utf8') as f:
            self.prompt = f.read()
        # 支持自定义 API key 和 base url
        openai.api_key = settings['api_key']
        openai.base_url = settings['base_url']

        self.model_name = settings['model_name'] if 'model_name' in settings else 'o4-mini'

    # def reset(self):
    #     self.log_path = f'{log_dir}/{self.sample_name}_{datetime.now().strftime("%Y%m%d-%H%M%S")}.tsv'

    def chat(self, message=None):
        # 初始化对话历史
        if not hasattr(self, 'history'):
            self.history = []
            self.history.append({"role": "user", "content": self.prompt})

        # 如果有用户输入，加入历史
        elif message != None:
            self.history.append({"role": "user", "content": message})
            log("user", message, self.log_path)

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
    
# class LLM_Chat():
#     def __init__(self):
#         self.file_name = "闪电_社交性高_能动性低"
#         with open(f'content/{self.file_name}.txt', 'r', encoding='utf8') as f:
#             self.content = f.readlines()
#         self.chat_dict = {}
#         log_dir = tomli.load(open('settings.toml', 'rb'))['log_dir']
#         self.log_path = f'{log_dir}/{self.file_name}_{datetime.now().strftime("%Y%m%d-%H%M%S")}.tsv'
#         self.idx = 0
#         self.instr = None
#         self.action = None
#         self.resp = None
#         self.stop = False

#     def reset(self):
#         self.log_path = f'{log_dir}/{self.file_name}_{datetime.now().strftime("%Y%m%d-%H%M%S")}.tsv'
#         self.idx = 0
#         self.instr = None
#         self.action = None
#         self.resp = None
#         self.stop = False

#     def chat(self, message=None):
#         if self.stop: return json.dumps({"type": "error", "content": "会话已结束,请刷新页面重新开始"})
#         if message:
#             try:
#                 # 没有继续的instr，就是None
#                 text, new_dict, self.instr = self.resp.execute(message)
#             except ValueError as e:
#                 text = str(e)
#                 print(f"错误: {text}")
#                 self.stop = True
#                 return json.dumps({"type": "error", "content": text})

#             resp_name = self.resp.__class__.__name__
#             log(resp_name, text, self.log_path)

#             if new_dict: self.chat_dict |= new_dict

#         try:
#             return json.dumps({"type": "chat", "content": self.get_chat_text()})
#         except ValueError as e:
#             return json.dumps({"type": "error", "content": str(e)})

#     def chat_start(self):
#         self.reset()
#         return self.chat()

#     def get_chat_text(self):
#         new_resp = False
#         if not self.instr:
#             new_resp = True
#             if self.idx < len(self.content):
#                 self.instr = self.content[self.idx]
#                 self.idx += 1
#             else:
#                 self.stop = True
#                 raise ValueError("会话已结束,请刷新页面重新开始")
#         self.instr = self.instr.strip()
#         if self.instr.startswith('chat:'):
#             self.action = Chat(self.instr[5:].strip())
#             if new_resp: self.resp = Chat_Resp()
#         elif self.instr.startswith('exam:'):
#             self.action = Exam(self.instr[5:].strip())
#             if new_resp: self.resp = Exam_Resp()
#         elif self.instr.startswith('name:'):
#             self.action = Name(self.instr[5:].strip())
#             if new_resp: self.resp = Name_Resp()
#         else:
#             print(self.instr)
#             raise ValueError(f"不支持的动作")
        
#         text, _, self.instr = self.action.execute(self.chat_dict)
#         role = self.action.__class__.__name__
#         log(role, text, self.log_path)
#         return text

#     def __str__(self):
#         return f'{self.log_path}'

class LLMChatFactory:
    """LLM聊天工厂类"""
    @staticmethod
    def create_llm_chat(sample_name) -> LLM_Chat:
        """
        创建LLM聊天实例的工厂方法
        
        Returns:
            LLM_Chat实例
        """
        return LLM_Chat(sample_name)
    # @staticmethod
    # def create_llm_chat(topic, sociability, initiativity) -> LLM_Chat:
    #     """
    #     创建LLM聊天实例的工厂方法
        
    #     Args:
    #         chat_type: 聊天类型，默认为"default"
            
    #     Returns:
    #         LLM_Chat实例
    #     """
    #     if topic == 'thunder' and sociability == 'high' and initiativity == 'low':
    #         return LLM_Chat()
    #     else:
    #         # 提供更具体的错误信息
    #         raise ValueError(f"不支持的聊天组合: topic='{topic}', sociability='{sociability}', initiativity='{initiativity}'")

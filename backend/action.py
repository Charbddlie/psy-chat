import argparse
import pandas as pd
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
import re
import os
import tomli

def format_output(text, chat_dict):
    # 检查文本中是否包含变量标记
    
    # 使用正则表达式找出所有 {变量名} 形式的标记
    variables = re.findall(r'\{(\w+)\}', text)
    
    # 如果存在变量标记
    if variables:
        # 检查所有变量是否都在chat_dict中存在
        missing_vars = [var for var in variables if var not in chat_dict]
        if missing_vars:
            # 如果有缺失变量，抛出错误
            raise ValueError(f"在chat_dict中找不到以下变量: {', '.join(missing_vars)}")
        
        # 所有变量都存在，进行格式化
        return text.format(**chat_dict)
        
    else:
        # 如果没有变量标记，直接打印原文本
        return text

class Action(ABC):
    def __init__(self, text=None, suffix=''):
        self.text = text
        self.suffix = suffix

    @abstractmethod
    def execute(self, chat_dict):
        text = format_output(self.text, chat_dict)
        return text + self.suffix, None, None

with open('settings.toml', 'rb') as f:
    settings = tomli.load(f)

class Chat(Action):
    def __init__(self, text=None):
        super().__init__(text, suffix=settings['chat'])

class Exam(Action):
    def __init__(self, text=None):
        super().__init__(text, suffix=settings['exam'])

class Name(Action):
    def __init__(self, text=None):
        super().__init__(text, suffix=settings['name'])

    

# text, dict, retry_info
class Chat_Resp():
    def __init__(self, resp_list=['有', '没有'], max_retry=3):
        self.resp_list = resp_list
        self.max_retry = max_retry
        self.cnt = max_retry

    def execute(self, resp):
        if self.cnt > 0:
            if resp in self.resp_list:
                self.cnt = self.max_retry
            else:
                self.cnt -= 1
                return f'{resp}(输入错误)', None, f"chat:输入错误，请重新输入，你还有{self.cnt}次机会"
        else:
            raise ValueError("输入错误次数过多，请刷新重新开始")

        return resp, None, None

class Exam_Resp():
    def __init__(self, answer_format='(1.xx 2.xx 3.xx)'):
        self.answer_format = answer_format

    def execute(self, answer):
        return answer, None, None

class Name_Resp():
    def __init__(self):
        pass

    def execute(self, name):
        return name, {'name': name}, None

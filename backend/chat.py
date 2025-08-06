import os
from dataclasses import dataclass
from datetime import datetime
import asyncio
import os
import datetime
import tomli
from openai import AsyncOpenAI  # 使用异步客户端
import aiofiles  # 异步文件操作，替代同步IO

log_dir = tomli.load(open('settings.toml', 'rb'))['log_dir']
settings = tomli.load(open('settings.toml', 'rb'))

class LLMChat():
    # 类级别的信号量，限制并发API请求数量
    api_semaphore = asyncio.Semaphore(settings['api_semaphore'])
    chat_test = settings['chat_test']

    def __init__(self, user_name, user_id):
        self.chat = self.test_chat if LLMChat.chat_test else self.ai_chat

        self.user_name = user_name
        self.user_id = user_id
        self.log_dir = f"{settings['log_dir']}/{user_name}_{user_id}"
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_path = os.path.join(self.log_dir, "chat.tsv")
        
        # 读取prompt（同步操作，初始化时执行一次影响较小）
        with open('prompt/thunder_prompt.txt', 'r', encoding='utf8') as f:
            self.prompt = f.read().replace('{name}', user_name)
        
        # 初始化异步OpenAI客户端（关键改进）
        self.client = AsyncOpenAI(
            api_key=settings['api_key'],
            base_url=settings['base_url'],
            timeout=10.0  # API超时设置（全局生效）
        )
        
        self.model_name = settings.get('model_name', 'o4-mini')
        self.history = [{"role": "user", "content": self.prompt}]

        has_content = False
        # 在初始化时从log_path读取历史聊天记录（除去第一条prompt），同步方式即可
        if os.path.exists(self.log_path):
            with open(self.log_path, "r", encoding="utf8") as f:
                lines = f.readlines()
            if lines:
                header = lines[0].rstrip("\n").split("\t")
                role_idx = header.index("role") if "role" in header else None
                text_idx = header.index("text") if "text" in header else None
                # 跳过header，从第二行开始
                for line in lines[1:]:
                    has_content = True
                    fields = line.rstrip("\n").split("\t")
                    if len(fields) < max(role_idx, text_idx) + 1: continue
                    role = 'assistant' if fields[role_idx] == 'AI' else 'user'
                    text = fields[text_idx].replace("\\n", "\n")
                    # 跳过第一条prompt（已在self.history[0]）
                    self.history.append({"role": role, "content": text})
        if not has_content:
            with open(self.log_path, "w", encoding="utf8") as f:
                f.write("role\ttext_len\ttime\ttext\n")
        

    async def save_line(self, role, text, time):
        """生成一条符合格式的日志记录（dict）"""
        record_data = {
            'role': role,
            'text_len': str(len(text)),
            'time': str(time),
            'text': text.replace('\n', '\\n'),
        }
        # 清理制表符
        record_data = {k: v.strip().replace('\t', '    ') for k, v in record_data.items()}
        line = '\t'.join(record_data.values()) + '\n'
        async with aiofiles.open(self.log_path, 'a', encoding='utf8') as f:
            await f.write(line)
        return line

    async def ai_chat(self, message=None):
        """处理聊天请求的异步函数（改进版）"""
        try:            
            # 处理用户输入
            if message is not None:
                self.history.append({"role": "user", "content": message})

                # 生成日志记录
                log_time = datetime.datetime.now().isoformat()
                await self.save_line("user", message, log_time)  # 直接调用异步保存（无需线程池）
            
            # 记录当前历史长度，用于检查是否为过时回复
            next_idx = len(self.history)
            
            # 使用信号量限制并发
            async with LLMChat.api_semaphore:
                try:
                    # 异步调用OpenAI API（关键改进）
                    stream = await self.client.chat.completions.create(
                        model=self.model_name,
                        messages=self.history,
                        stream=True,
                    )
                    
                    ai_message = ""
                    # 异步迭代流式响应（关键改进）
                    async for chunk in stream:  # 使用async for处理异步迭代器
                        if not chunk.choices:
                            continue
                        delta = chunk.choices[0].delta.content
                        if delta:
                            ai_message += delta
                            yield delta
                            
                    if not ai_message:
                        raise ValueError("API未返回有效内容")

                    # 检查是否为过时回复（避免历史已更新时追加旧回复）
                    if next_idx != len(self.history):
                        return
                        
                    # 记录AI回复
                    self.history.append({"role": "assistant", "content": ai_message})
                    
                    # 生成AI日志
                    log_time = datetime.datetime.now().isoformat()
                    await self.save_line("AI", ai_message, log_time)
                    
                except Exception as e:
                    print(f"API调用错误: {e}")
                    raise
                    
        except Exception as e:
            print(f"聊天处理错误: {e}")
            raise  

    # chat test
    async def test_chat(self, message=None):
        """
        仅用于测试的chat接口，不调用AI，仅记录用户消息并返回固定回复。
        """
        try:
            if message is not None:
                self.history.append({"role": "user", "content": message})

                # 生成日志记录
                log_time = datetime.datetime.now().isoformat()
                await self.save_line("user", message, log_time)

            # 生成一个固定的AI回复
            ai_message = "（测试模式）收到消息：" + (message if message is not None else "")
            self.history.append({"role": "assistant", "content": ai_message})

            # 生成AI日志
            log_time = datetime.datetime.now().isoformat()
            await self.save_line("AI", ai_message, log_time)

            # 模拟流式返回
            for delta in ai_message:
                yield delta

        except Exception as e:
            print(f"测试聊天处理错误: {e}")
            raise

    def get_history(self):
        """获取聊天历史，跳过第一条提示信息"""
        if not hasattr(self, 'history') or self.history is None:
            return []
            
        result = []
        for item in self.history[1:]:
            new_item = item.copy()
            result.append(new_item)
        return result

    def __str__(self):
        return f'{self.log_path}'
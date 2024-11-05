from typing import List
import dotenv
import os
from openai import OpenAI

from react_agent.memory import Message

dotenv.load_dotenv()


class BaseModel:
    def __init__(self, path: str = '') -> None:
        self.path = path

    def chat(self, prompt: str, history: List[dict]):
        pass

    def load_model(self):
        pass


class OpenAIChat(BaseModel):
    def __init__(self, path: str = '', **kwargs) -> None:
        super().__init__(path)
        self.load_model(**kwargs)
        self.history: List[Message] = []
        self.kwargs = kwargs

    def load_model(self, **kwargs):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE"),
        )

    def chat(self, prompt: str, history: List[Message], meta_instruction: str = '', tools=None) -> str:
        """
        normal chat
        """
        if tools is None:
            tools = {}
        is_verbose = self.kwargs.get('is_verbose', True)   # 流式输出
        messages = []

        # 添加历史对话信息
        history_dict = [dict(h) for h in history]
        messages.extend(history_dict[-6:])  # 最新的 3 组对话

        # 拼接 系统提示词
        if meta_instruction:
            messages.append({"role": "system", "content": meta_instruction})

        messages.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(
            messages=messages,
            stream=True,
            tools=tools,
            tool_choice="auto",
            **self.kwargs
        )
        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                if is_verbose:
                    print(chunk.choices[0].delta.content, end="")
                full_response += chunk.choices[0].delta.content
        if is_verbose:
            print()
        return full_response


if __name__ == '__main__':
    model = OpenAIChat(model='qwen-max', temperature=1, stop=['\n'])
    print(model.chat('输出一个唐诗', []))

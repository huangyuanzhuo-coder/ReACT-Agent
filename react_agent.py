import sys
import os



print(os.getcwd())
print(os.path.join(os.getcwd(), "tools"))
sys.path.append(os.path.abspath(os.getcwd()))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "tools")))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union
import json5
from chat_model import OpenAIChat
from tool_registry import ToolRegistry, Tools
from prompts import REACT_PROMPT, TOOL_DESC
from memory import Message
from tool_funcs import calculator, google_search, government_law_knowledgeBase


class ReactAgent:
    def __init__(self, **kwargs) -> None:
        self.tools = Tools()
        kwargs['model'] = kwargs.get('model', 'qwen-max')
        kwargs['stop'] = kwargs.get('stop', ['\n'])
        kwargs['temperature'] = kwargs.get('temperature', 0)
        self.kwargs = kwargs
        self.model = OpenAIChat(**kwargs)
        print("model info:", kwargs)
        self.hit_final_answer = False

    def build_system_input(self, query, extra_requirements):
        tool_descs, tool_names = [], []
        for tool in self.tools.toolConfig:
            tool_descs.append(TOOL_DESC.format(**tool))
            tool_names.append(tool['name_for_model'])
        tool_descs = '\n\n'.join(tool_descs)
        tool_names = ','.join(tool_names)
        sys_prompt = REACT_PROMPT.format(tool_descs=tool_descs,
                                         tool_names=tool_names,
                                         current_date=datetime.now().strftime("%Y-%m-%d"),
                                         query=query,
                                         extra_requirements=extra_requirements)

        return sys_prompt

    def parse_latest_plugin_call(self, text):
        """查找最后一个 Tool Invocation 和 Tool Input"""
        tool_invocation = text.split('Action:')[-1].split('\n')[0].strip()
        tool_input = text.split('Action Input:')[-1].split('\n')[0].strip()

        return tool_invocation, tool_input

    def call_plugin(self, plugin_name, plugin_args):
        try:
            plugin_args = json5.loads(plugin_args)
        except Exception as e:
            return '\nObservation:' + f"输入解析错误：{str(e)} 请检查输入参数是否正确"

        try:
            return '\nObservation:' + str(self.tools.execute_tool(plugin_name, **plugin_args))
        except Exception as e:
            return '\nObservation:' + f"工具执行出错：{str(e)} 请检查输入参数是否正确"

    def step(self, scratchpad):
        return self.model.chat(scratchpad, self.model.history, self.system_prompt)

    def run(self, query, extra_requirements=""):
        # 构建系统提示词
        self.system_prompt = self.build_system_input(query, extra_requirements)
        # print("system_prompt:", self.system_prompt)

        # 初始化scratchpad
        scratchpad = ""
        print(self.model.history)
        while True:
            response = self.step(scratchpad)  # 获取下一个响应[Analysis, Tool Invocation, Tool Input, Tool Output]

            if response.startswith("Thought:"):
                pass
            elif response.startswith("Action Input:"):
                plugin_name, plugin_args = self.parse_latest_plugin_call(scratchpad + '\n' + response)
                print("using tool:", plugin_name)
                print("using args:", plugin_args)
                delta = self.call_plugin(plugin_name, plugin_args)
                # print("delta:", delta)
                response += delta
                # print("response:", response)
            elif response.startswith("Action:"):
                pass

            # 异常控制
            elif response.startswith("Observation:"):
                response = "you shouldn't get Observation by yourself, you should get it from the tools"

            elif response.startswith("Final Answer:"):
                # 取消只能输出一行的限制(stop=['\n'])，重新获取response
                self.kwargs['stop'] = None
                self.model.kwargs = self.kwargs
                response = self.step(scratchpad)
                print(response)

                # 添加当前轮次对话
                self.model.history.append(Message(role="user", content=query))
                self.model.history.append(Message(role="system", content=response))
                return response

            else:
                response = ("Invalid Output prefix, please use one of the following the next time: [Thought, Action, "
                            "Action Input, Observation]")

            print(response)
            scratchpad += '\n' + response



if __name__ == '__main__':
    agent = ReactAgent(model="qwen-max", temperature=1)

    agent.tools.add_tool(
        name_for_human="calculator",
        name_for_model="calculator",
        func=calculator,
        description="calculator是一个用于进行数学计算的工具。",
        parameters=[
            {
                'name': 'expression',
                'description': '可以被python eval 函数执行的数学表达式',
                'required': True,
                'schema': {'type': 'string'},
            }
        ]
    )
    agent.tools.add_tool(
        name_for_human="google search",
        name_for_model="google_search",
        func=google_search,
        description="google search是一个通用搜索引擎，可用于访问互联网、查询百科知识、了解时事新闻等。",
        parameters=[
            {
                'name': 'search_query',
                'description': '搜索关键词或短语',
                'required': True,
                'schema': {'type': 'string'},
            }
        ]
    )
    agent.tools.add_tool(
        name_for_human='government_law_knowledgeBase',
        name_for_model='government_law_knowledgeBase',
        func=government_law_knowledgeBase,
        description='government_law_knowledgeBase一个文档知识库，用于查询法律、政府文件的相关内容。',
        parameters=[
            {
                'name': 'search_query',
                'description': '搜索关键词或短语',
                'required': True,
                'schema': {'type': 'string'},
            }
        ],
    )

    result = agent.run("保密法的第三条和第四条有什么区别？")
    print("-" * 150)
    agent.run("第十一条是什么？")
    # result = agent.run(input("请输入问题："), extra_requirements=input("请输入额外要求："))
    # print(result)

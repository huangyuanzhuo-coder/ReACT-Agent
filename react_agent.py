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
from prompts import REACT_PROMPT, TOOL_DESC, REFINE_PROMPT, TEST_DOC
from memory import Message
from tool_funcs import calculator, google_search, government_law_knowledgeBase, context_generator


class ReactAgent:
    def __init__(self, **kwargs) -> None:
        self.tools = Tools()
        kwargs['model'] = kwargs.get('model', 'qwen-max')
        kwargs['stop'] = kwargs.get('stop', ['\n'])
        kwargs['temperature'] = kwargs.get('temperature', 1)
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
        # print(self.model.history)

        scratchpad = ""
        while True:
            response = self.step(scratchpad)  # 获取下一个响应[Analysis, Tool Invocation, Tool Input, Tool Output]

            if response.startswith("Thought:") or response.startswith("Action:"):
                pass
            elif response.startswith("Action Input:"):
                plugin_name, plugin_args = self.parse_latest_plugin_call(scratchpad + '\n' + response)
                # print("using tool:", plugin_name)
                # print("using args:", plugin_args)
                obs = self.call_plugin(plugin_name, plugin_args)
                print(obs)
                response += obs
            elif response.startswith("Final Answer:"):
                # 取消只能输出一行（下一step）的限制(stop=['\n'])，重新获取response
                self.kwargs['stop'] = None
                self.model.kwargs = self.kwargs
                response = self.step(scratchpad)
                self.kwargs['stop'] = ['\n']

                # 添加当前轮次对话
                self.model.history.append(Message(role="user", content=query))
                self.model.history.append(Message(role="system", content=response.split("Final Answer: ")[1]))

                return response

            # 异常控制
            elif response.startswith("Observation:"):
                response = "you shouldn't get Observation by yourself, you should get it from the tools"
            else:
                response = ("Invalid Output prefix, please use one of the following the next time: [Thought, Action, "
                            "Action Input, Observation]")

            # print(response)
            print("-" * 100)
            scratchpad += '\n' + response


if __name__ == '__main__':
    agent = ReactAgent(model="qwen-max", temperature=1)

    # 注册工具
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
        description='government_law_knowledgeBase是一个文档知识库，用于查询法律、政府文件的相关内容。',
        parameters=[
            {
                'name': 'search_query',
                'description': '搜索关键词或短语',
                'required': True,
                'schema': {'type': 'string'},
            }
        ],
    )
    agent.tools.add_tool(
        name_for_human='context_generator',
        name_for_model='context_generator',
        func=context_generator,
        description='context_generator用于生成指定领域和类型的文档',
        parameters=[
            {
                'name': 'area',
                'description': '文件的领域、事件',
                'required': True,
                'schema': {'type': 'string'},
            },
            {
                'name': 'doc_type',
                'description': '文件的类型',
                'required': True,
                'schema': {'type': 'string'},
            }
        ],
    )

    # 测试反思
    prompt = REFINE_PROMPT.format(doc=TEST_DOC)

    result = agent.run("我想生成一个有关中美关系局势紧张的新闻")
    print("-" * 150)
    # agent.run("第十一条是什么？")
    # result = agent.run(input("请输入问题："), extra_requirements=input("请输入额外要求："))
    # print(result)

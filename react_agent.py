import sys
import os
import json5
from datetime import datetime
print(sys.path)
print(os.getcwd())
sys.path.append(os.path.abspath(os.getcwd()))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from react_agent.memory import Message
from react_agent.function_call.register.functionsRegistry import FunctionsRegistry
from react_agent.prompt.prompts import REACT_PROMPT, REFINE_PROMPT, TEST_DOC
from chat_model import OpenAIChat


class ReactAgent:
    def __init__(self, **kwargs) -> None:
        # self.tools = Tools()
        self.tools = FunctionsRegistry()
        kwargs['model'] = kwargs.get('model', 'qwen-plus')
        kwargs['stop'] = kwargs.get('stop', ['\n'])
        kwargs['temperature'] = kwargs.get('temperature', 1)
        self.kwargs = kwargs
        self.model = OpenAIChat(**kwargs)
        print("model info:", kwargs)
        self.hit_final_answer = False

    def build_system_input(self, query, extra_requirements):
        # tool_descs, tool_names = [], []
        # for tool in self.tools.toolConfig:
        #     tool_descs.append(TOOL_DESC.format(**tool))
        #     tool_names.append(tool['name_for_model'])
        # tool_descs = '\n\n'.join(tool_descs)
        # tool_names = ','.join(tool_names)
        sys_prompt = REACT_PROMPT.format(
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
            # return '\nObservation:' + str(self.tools.execute_tool(plugin_name, **plugin_args))
            return '\nObservation:' + str(self.tools.get_function_callable()[plugin_name](**plugin_args))
        except Exception as e:
            return '\nObservation:' + f"工具执行出错：{str(e)} 请检查输入参数是否正确"

    def step(self, scratchpad):
        return self.model.chat(scratchpad, self.model.history, self.system_prompt, self.tools.mapped_functions())

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

    result = agent.run("刘强东创办京东时多少岁？")
    print("-" * 150)
    result = agent.run("奶茶妹呢？")


    # 测试反思
    prompt = REFINE_PROMPT.format(doc=TEST_DOC)
    # agent.run("第十一条是什么？")
    # result = agent.run(input("请输入问题："), extra_requirements=input("请输入额外要求："))
    # print(result)

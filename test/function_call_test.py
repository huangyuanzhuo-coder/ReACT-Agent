import os
import logging
import json
import dotenv
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv

from react_agent.function_call.register.functionsRegistry import FunctionsRegistry

dotenv.load_dotenv()
# Set up logging
logging.basicConfig(level=logging.INFO)


def main() -> None:
    load_dotenv()
    question = (
            "大唐华银电力股份有限公司法人代表是谁")
    # question = ""
    try:
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE"),
        )

        tools = FunctionsRegistry()
        print(tools.mapped_functions())
        function_map = tools.get_function_callable()

        messages: List[Dict[str, str]] = [
            {"role": "user", "content": f"{question}"}
        ]
        completion = client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            tools=tools.mapped_functions(),
            tool_choice="auto",
        )

        response_message = completion.choices[0].message
        print(response_message)
        # 依据问题选择需要调用的函数列表
        tool_calls = response_message.tool_calls

        if tool_calls:
            # messages.append(response_message)
            # 遍历所有的可调用的函数
            for tool_call in tool_calls:
                # 获取函数名称
                function_name = tool_call.function.name
                print(function_name)
                if function_name in function_map:
                    # 获取函数参数
                    function_args = json.loads(tool_call.function.arguments)
                    print(function_args)
                    try:
                        # 函数返回的结果
                        function_response = function_map[function_name](
                            **function_args)
                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        })
                    except Exception as e:
                        logging.error(f"Error in {function_name}: {e}")

            second_completion = client.chat.completions.create(
                model="qwen-plus",
                messages=messages
            )
            print(second_completion)
            logging.info(second_completion)
        else:
            print("没有工具调用")
            logging.info(completion)

    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

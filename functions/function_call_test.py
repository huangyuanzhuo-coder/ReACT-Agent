from typing import List, Dict, Any
import dotenv
from openai import OpenAI
from dotenv import load_dotenv
import os
import logging
import json

dotenv.load_dotenv()
from functions.functionsRegistry import FunctionsRegistry

# Set up logging
logging.basicConfig(level=logging.INFO)


def main() -> None:
    load_dotenv()
    question = (
            "大唐华银电力股份有限公司法人与上海现代制药股份有限公司发生了民事纠纷，大唐华银电力股份有限公司委托给了北京国旺律师事务所，" +
            "上海现代制药股份有限公司委托给了北京浩云律师事务所" +
            "请写一份民事起诉状给天津市蓟州区人民法院时间是2024-02-01，注：法人的地址电话可用公司的代替。")
    # question = ""
    try:
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE"),
        )

        tools = FunctionsRegistry()
        function_map = tools.get_function_callable()

        messages: List[Dict[str, str]] = [
            {"role": "user", "content": f"{question}"}
        ]
        completion = client.chat.completions.create(
            model="qwen-max",
            messages=messages,
            tools=tools.mapped_functions(),
            tool_choice="auto",
        )

        response_message = completion.choices[0].message
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
                model="qwen-max",
                messages=messages
            )

            logging.info(second_completion)
        else:
            logging.info(completion)

    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

import os
import json
import requests
import dotenv

from chat_model import OpenAIChat
from rag.simple_rag import RAG_search

dotenv.load_dotenv()


# 添加计算器工具
def calculator(expression: str):
    return eval(expression)


# 添加谷歌搜索工具
def google_search(search_query: str):
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": search_query})
    headers = {
        'X-API-KEY': os.getenv('SERPER_API_KEY'),
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    return response['organic'][0]['snippet']


def government_law_knowledgeBase(search_query: str):
    return RAG_search(search_query)


def context_generator(outline, area, doc_type):
    prompt = f"""你是一个文件生成助手，你的任务是根据用户提供的文件类型和领域生成虚拟的文件中的一部分。
    主编的文件要求如下：
    1、应当在文档中出现这个文件类型应当有的内容、格式或者说辞：
    2、生成的文件不应该对其中的任何内客进行解释
    3、文件中应当基于文件的领域和类型生成一个虚构的故事，保证故事的合理性、相关性和连贯性：
    4、如果需要生成一个人物。请合理虚构他的身份信息：
    5、生成内寄中的单位、部门、公司等信息时，不要出现任何模糊说法或指代说法，如某单位、XX单位、A单位等。请你用虚构具体的实体代警：
    6，这不是生成一个模板，这是生成一个真实的文件，请不要出现模糊、指代、未确定的说法：
    7、生成具体内容时，尽量采用大段的阐述信息
    8．尽可能的丰富文件中不同部分的内容，同时保证内容的质量。
    9.文件的字数控制在3000字左右
    
    生成的部分{outline}
    文件类型：{doc_type}
    文件领域：{area}
    
    生成的内容：
"""
    kwargs = {}
    kwargs['model'] = kwargs.get('model', 'qwen-max')
    kwargs['stop'] = kwargs.get('stop', ['\n'])
    kwargs['temperature'] = kwargs.get('temperature', 1)
    kwargs = kwargs
    model = OpenAIChat(**kwargs)
    res = model.chat("", model.history, prompt)

    print(res)


if __name__ == '__main__':
    context_generator("目录", "招标书", "人民公园建设招标书")


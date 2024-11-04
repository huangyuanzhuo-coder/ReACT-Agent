import os
import json
import requests
import dotenv
from prompts import CONTEXT_GENERATION_PROMPT, OUTLINE_PROMPT, PART_PROMPT, REFINE_PROMPT
from chat_model import OpenAIChat
from md2docx import md_to_docx
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


def context_generator(area, doc_type):
    context_generator_prompt = CONTEXT_GENERATION_PROMPT.format(doc_type=doc_type,
                                                                area=area)

    model = OpenAIChat(model='qwen-max', temperature=1)
    res = model.chat("", [], context_generator_prompt)

    # 保存文件
    md_to_docx(res, f"./docs/{area}：{doc_type}.docx")
    with open(f"./docs/{area}：{doc_type}.md", "w") as f:
        f.write(res)

    return res


def outline_generator(area, doc_type):
    doc_prompt = f"""
文件类型：{doc_type}
文件领域：{area}

组成部分：
    """
    outline_prompt = OUTLINE_PROMPT + doc_prompt

    model = OpenAIChat(model='qwen-max', temperature=1)
    res = model.chat("", [], outline_prompt)

    return res


def partition_generator(area, doc_type, outline):
    doc_prompt = f"""
文件类型：{doc_type}
文件领域：{area}

组成部分：
"""
    part_prompt = PART_PROMPT + doc_prompt

    model = OpenAIChat(model='qwen-max', temperature=1)
    res = model.chat("", [], part_prompt)

    return res


def refine_doc(doc):
    refine_prompt = REFINE_PROMPT.format(doc=doc)

    model = OpenAIChat(model='qwen-max', temperature=1)
    res = model.chat("", [], refine_prompt)

    return res


if __name__ == '__main__':
    # context_generator("正文", "工作秘密", "定向电磁调制设备核心原理")

    outline_generator("通知", "保密项目实施条例")

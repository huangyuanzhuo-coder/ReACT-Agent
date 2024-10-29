import os, json
import requests
from rag.simple_rag import RAG_run

"""
工具函数

- 首先要在 tools 中添加工具的描述信息
- 然后在 tools 中添加工具的具体实现

- https://serper.dev/dashboard
"""


class Tools:
    def __init__(self) -> None:
        self.toolConfig = self._tools()

    def _tools(self):
        tools = [
            {
                'name_for_human': '谷歌搜索',
                'name_for_model': 'google_search',
                'description_for_model': '谷歌搜索是一个通用搜索引擎，可用于访问互联网、查询百科知识、了解时事新闻等。',
                'parameters': [
                    {
                        'name': 'search_query',
                        'description': '搜索关键词或短语',
                        'required': True,
                        'schema': {'type': 'string'},
                    }
                ],
            },
            # 计算器
            {
                'name_for_human': '计算器',
                'name_for_model': 'calculator',
                'description_for_model': '计算器是一个用于进行数学计算的工具。',
                'parameters': [
                    {
                        'name': 'expression',
                        'description': '可以被python eval 函数执行的数学表达式',
                        'required': True,
                        'schema': {'type': 'string'},
                    }
                ],
            },
            # RAG
            {
                'name_for_human': '法律、政府知识库',
                'name_for_model': 'government_law_knowledgeBase',
                'description_for_model': '法律、政府知识库一个文档知识库，用于查询法律、政府文件的相关内容。',
                'parameters': [
                    {
                        'name': 'search_query',
                        'description': '搜索关键词或短语',
                        'required': True,
                        'schema': {'type': 'string'},
                    }
                ],
            }
        ]
        return tools

    def google_search(self, search_query: str):
        url = "https://google.serper.dev/search"

        payload = json.dumps({"q": search_query})
        headers = {
            'X-API-KEY': os.getenv('SERPER_API_KEY'),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()

        return response['organic'][0]['snippet']

    def calculator(self, expression: str):
        return eval(expression)

    def government_law_knowledgeBase(selfself, search_query: str):
        return RAG_run(search_query)


if __name__ == '__main__':
    tool = Tools()
    print(tool.google_search('python'))

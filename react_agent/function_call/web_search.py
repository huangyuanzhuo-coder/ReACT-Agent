import json
import os
import requests

from react_agent.function_call.register.functions_metadata import function_schema


@function_schema(
    name="google_search",
    description="google search是一个通用搜索引擎，可用于访问互联网、查询百科知识、了解时事新闻等。",
    required_params=["search_query"]
)
def google_search(search_query: str):
    """
    :param search_query: 搜索关键词或短语
    """
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": search_query})
    headers = {
        'X-API-KEY': os.getenv('SERPER_API_KEY'),
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    return response['organic'][0]['snippet']

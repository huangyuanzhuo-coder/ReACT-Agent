from react_agent.function_call.register.functions_metadata import function_schema
from react_agent.function_call.tools.rag.simple_rag import RAG_search


@function_schema(
    name="government_law_knowledgeBase",
    description="government_law_knowledgeBase是一个文档知识库，用于查询法律、政府文件的相关内容。",
    required_params=["search_query"]
)
def government_law_knowledgeBase(search_query: str):
    """
    :param search_query: 搜索关键词或短语
    """
    return RAG_search(search_query)

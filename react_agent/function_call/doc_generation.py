from chat_model import OpenAIChat
from react_agent.function_call.register.functions_metadata import function_schema
from react_agent.function_call.tools.md2docx import md_to_docx
from react_agent.prompt.prompts import CONTEXT_GENERATION_PROMPT, OUTLINE_PROMPT, PART_PROMPT, REFINE_PROMPT


@function_schema(
    name="context_generator",
    description="context_generator用于生成指定领域和类型的文档",
    required_params=["area", "doc_type"]
)
def context_generator(area, doc_type):
    """
    :param area: 文件的领域、事件
    :param doc_type: 文件的类型
    """
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

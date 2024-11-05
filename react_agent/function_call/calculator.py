from react_agent.function_call.register.functions_metadata import function_schema


@function_schema(
    name="calculator",
    description="calculator是一个用于进行数学计算的工具。",
    required_params=["expression"]
)
def calculator(expression: str):
    """
    :param expression: 可以被python eval 函数执行的数学表达式
    """
    return eval(expression)

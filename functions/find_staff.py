import sys

from functions.functions_metadata import function_schema

print(sys.path)
import os
print(os.environ.get('PYTHONPATH'))
import functions.functionsRegistry



@function_schema(
    name="find_staff",
    description="通过名字和姓氏查找员工",
    required_params=["first_name", "last_name"]
)
def find_staff(first_name: str, last_name: str):
    """
    :param first_name: 搜索中显示的员工名字（名）
    :param last_name: 搜索中显示的员工姓氏
    """
    return f"员工为：{first_name}{last_name}"

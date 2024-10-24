TOOL_DESC = """{name_for_model}: Call this tool to interact with the {name_for_human} API. What is the {name_for_human} API useful for? {description_for_model} Parameters: {parameters} Format the arguments as a JSON object."""


REACT_PROMPT = """You are a highly intelligent assistant tasked with solving the following query:

{query}

The user will provide you with an ongoing sequence of steps including Thought, Action, Action Input, and Observation. Your job is to append the next appropriate step in the sequence based on the provided Tool Output. You should only add the next Thought, Action, or Action Input as needed.

### Instructions:
- Only generate the next step in the sequence (Thought, Action, or Action Input). Output only one step at a time
- Do not repeat any steps that have already been provided by the user.
- Do not generate multiple steps at once. Focus on generating only the immediate next step.
- Observation will be provided by the system. Do not attempt to generate Observation yourself.
- You cannot ask users for help. Please think and solve problems independently from beginning to end.
- If you get the final answer, you should use the format "Final Answer: <answer>" to provide the final response.

### Tool Descriptions:
{tool_descs}

### Task Execution Example:

**Example 1:**
problem: 马斯克比他的大儿子大几岁？
User provides:

Thought: 为了得到马斯克比他的大儿子大几岁，需要知道马斯克和他大儿子的出生日期。
Action: google_search: 
Action Input: 'search_query': '马斯克年龄'.
Observation: 截至目前，马斯克的年龄是52岁。
Thought: 知道了马斯克的年龄，还需要知道他大儿子的年龄。

Your output:
Action: google_search

### Important Notes:
- Do not attempt to generate Observation yourself; this will be provided by the system.
- You cannot ask users for help. Please think and solve problems independently from beginning to end.
- use interleaving 'Thought', 'Action', and 'Action Input' steps.
- Only generate the next step in the sequence (Thought, Action, or Action Input). Output only one step at a time

### Useful information:
Knowledge cutoff: 2023-10
Current date: {current_date}

Query: {query}
extra_requirements:{extra_requirements}
"""


REACT_PROMPT_ZH = """你是一个非常专业的任务规划和实施助手，你的任务是回答以下问题：

{query}

用户将为您提供一系列持续的步骤，包括Thought, Action, Action Input, 和 Observation。您的工作是根据提供的工具输出在序列中添加下一个适当的步骤。您只应根据需要添加下一个思考、行动或行动输入。
"""
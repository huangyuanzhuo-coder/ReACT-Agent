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
- Constructively self-criticize your big-picture behavior constantly.
- Reflect on past decisions and strategies to refine your approach.
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


CONTEXT_GENERATION_PROMPT = """你是一个优秀的多领域文件生成专家，你的任务是根据用户提供的文件类型和领域生成虚拟的文件中的某一部分。
生成文件的要求如下：
1. 应当在文档中出现这个文件类型应当有的内容、格式或者说辞：
2. 生成的文件不应该对其中的任何内客进行解释；
3. 文件中应当基于文件的领域和类型生成一个虚构的故事，保证故事的合理性、相关性和连贯性：
4. 如果需要生成一个人物。请合理虚构他的身份信息：
5. 生成内容中的单位、部门、公司等信息时，不要出现任何模糊说法或指代说法，如某单位、XX单位、A单位等。请你用虚构具体的实体代替：
6. 这不是生成一个模板，这是生成一个真实的文件，请不要出现模糊、指代、未确定的说法：
7. 生成具体内容时，尽量采用大段的阐述信息，不要生成太多的列举项；
8．尽可能的丰富文件中不同部分的内容，使各个部分的内容尽可能的多，同时保证内容的质量；
9. 文件的字数控制在3000字左右；

生成的部分：正文
文件类型：{doc_type}
文件领域：{area}

生成的内容：
"""

OUTLINE_PROMPT = """你是一个优秀的多领域文件生成专家，你的任务是根据用户提供的文件类型和领域判断生成这个虚拟的文件需要包含那些组成部分。
生成文件的要求如下：
1. 应当生成文件的各个组成部分和对该部分内容或格式的描述信息：
2. 相邻且内容较少的部分可以合并为一个组成部分
2. 生成的结果不应该对其中的任何内客进行解释；
4．尽可能的丰富文件中不同组成部分，使各个部分的内容更全面，同时保证内容的质量；
5. 返回的结果为json格式，确保可以被json.load()解析。

以下为几个示例:
通知:{"称呼":"对收信人的称呼，通常顶格写在信纸的第一行,要与署名对应，明确写信人与收信人的关系。",
"正文":"是信件的核心内容，用于表达写信人的意图和情感。正文通常分为连接语、主体文和总括语三个部分，每个部分开头都应另起一行，空两格落笔",
"署名和日期":"署名要写在信的右下角，前面可以加上合适的称谓，如“同学”、“好友”等。署名和日期之间可以加上一些客气用语，如“敬上”、“谨启”等。日期要写在具名的后边或者另起一行，通常写在信的右下角或下一行的右下方。"}

招标书:{"‌招标邀请函":"明确招标单位的名称、简介，确保投标单位了解招标项目的背景和要求。",
"投标人须知":"详细说明投标过程中需要注意的事项和具体的招标程序，确保投标过程的顺利进行。",
"资格、资信证明文件":"提供投标人的基本资质和资信证明，确保投标单位具备执行项目的能力。",
"‌投标报价要求":"详细说明投标报价的构成和计算方法，确保报价的合理性和准确性。",
"技术规格和要求":"明确项目的技术要求和标准，确保投标单位能够满足技术需求。",
"合同条件":"明确合同的主要条款和签订方式，保障双方的权益。",
"交货和服务时间":"明确交货和提供服务的时间安排，确保项目按时完成。",
"评标方法和标准":"明确评标的方法和标准，确保评标的公正性和客观性。",
"其他事项":"包括省级以上财政部门规定的其他事项，确保招标过程的合规性。"}

"""

PART_PROMPT = f"""你是一个优秀的多领域文件生成专家，你的任务是根据用户提供的文件类型和领域，生成这个文件中指定组成部分。
生成文件的要求如下：
1. 生成的部分应当只关注该组成部分在文档中涉及的内容、格式或者说辞：
2. 生成的内容不应该对其中的任何内客进行解释；

5. 生成内容中的单位、部门、公司等信息时，不要出现任何模糊说法或指代说法，如某单位、XX单位、A单位等。请你用虚构具体的实体代替：
6. 这不是生成一个模板，这是生成一个真实的文件，请不要出现模糊、指代、未确定的说法：
7. 生成具体内容时，尽量采用大段的阐述信息，不要生成太多的列举项；
8．尽可能的丰富这部分内容，同时保证内容的质量；

"""

REFINE_PROMPT = """你是一个优秀的多领域文档优化专家，你的任务是完善、优化给定的文档，使其更加的全面和真实。

优化的要求如下：
1. 你需要判断文档的各个部分的内容是不是足够多、足够完善，请你在需要扩充或者完善的地方进行修改；
2. 请你判断文档中是否有指代不明的信息。如果有，请将其替换为虚构的完整信息，并保证该信息在全文的一致性；
2. 直接生成完善后的文档，不要额外的解释

需要完善的文档如下：{doc}
"""

TEST_DOC = """### 举报信

尊敬的中央纪委国家监委信访室：

我是天华市财政局预算科科长李建，现年42岁，身份证号为110105198106053078。我怀着沉重的心情，向您举报我们天华市副市长赵志刚同志涉嫌严重贪污受贿及以权谋私的行为。以下是我掌握的具体情况和证据，请查证。

#### 赵志刚同志基本情况
赵志刚，男，1970年8月出生，中共党员，现任天华市人民政府副市长，分管城市建设、交通、环保等工作。自2018年起担任该职务以来，赵志刚在工作中表现出极强的权力欲望和贪婪本性，利用职务之便大肆敛财，严重影响了政府的形象和群众的利益。

#### 贪污受贿事实
1. **工程项目承包**
   - 2020年初，天华市启动了“环城路改造工程”，总预算达10亿元人民币。赵志刚通过其亲信王强（天华市城建局局长）与某私营企业主张伟（天华市金辉建筑公司总经理）私下接触，要求张伟支付20%的工程款作为“协调费”。最终，张伟通过银行转账的方式将2亿元打入赵志刚指定的账户。
   - 此外，赵志刚还利用其影响力，在其他多个市政工程项目中进行类似的“利益交换”，累计非法所得超过3亿元人民币。

2. **土地出让**
   - 2021年，天华市计划出让位于市中心的一块商业用地。赵志刚通过其妻子李红（天华市国土资源局副局长）与房地产开发商孙勇（天华市新天地地产集团董事长）达成协议，以低于市场价的价格将这块地出让给孙勇。事后，孙勇通过现金和名贵礼品的方式向赵志刚行贿，总价值约1亿元人民币。

3. **人事任免**
   - 赵志刚利用其分管人事的职权，多次干预下属部门的人事任免。例如，2022年，他将不具备相应资格的侄子赵雷安排到天华市税务局任副局长，并接受赵雷父母赠送的一套价值数百万元的别墅。
   - 同时，他还对那些不愿配合其非法行为的干部进行打压，如前任城建局局长刘涛因拒绝参与赵志刚的违法活动而被调离岗位，最终被迫辞职。

#### 以权谋私事实
1. **公款私用**
   - 赵志刚经常以公务考察名义，使用公款进行个人旅游和消费。例如，2021年，他以赴国外考察城市规划的名义，携家人前往欧洲旅游，所有费用均从市财政局报销，总计花费数十万元。
   - 另外，他还利用职务之便，为自己及其亲属购置多辆豪华轿车，并将其挂靠在市政府名下，用于日常出行。

2. **违规干预执法**
   - 2022年，赵志刚的儿子赵明因酒后驾车肇事，造成一死三伤的重大交通事故。事发后，赵志刚动用各种关系，干预司法机关的正常办案程序，导致赵明最终仅被判缓刑，未能得到应有的法律制裁。

#### 举报人信息及请求
我作为一名共产党员和公务员，深知廉洁自律的重要性。面对赵志刚同志如此严重的违法行为，我不能视而不见。为此，我已搜集并整理了大量相关证据材料，包括但不限于银行流水记录、录音录像资料以及多名目击者的证词。

请中央纪委国家监委对此事予以高度重视，并尽快立案调查，还天华市一个清廉的政治环境，维护人民群众的根本利益。本人愿意全力配合相关部门的调查工作，提供一切必要的协助和支持。

此致
敬礼！

举报人：李建  
联系电话：13800138000  
电子邮箱：lijian@thczj.com  
邮寄地址：天华市财政局预算科办公室  
邮政编码：100000  
日期：2023年10月1日

附件：
1. 银行流水记录复印件
2. 录音录像资料光盘
3. 目击者证词及相关材料
"""
# 项目简介

本项目是一个基于ReAct（Reasoning and Acting）框架的智能代理系统，能够通过调用不同的工具来回答用户的问题。主要功能包括谷歌搜索和计算器等。系统基于GPT-4模型，通过推理和行动的交互来生成答案。支持添加工具。

## 准备

1. 克隆项目代码：
    ```bash
    git clone https://github.com/huangyuanzhuo-coder/ReACT-Agent.git
    cd ReACT-Agent
    ```

2. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

3. 配置环境变量：
    在项目根目录下创建一个`.env`文件，并添加以下内容：
    ```env
    SERPER_API_KEY=<your_serper_api_key> # 使用谷歌搜索
    OPENAI_API_KEY=<your_openai_api_key>
    OPENAI_API_BASE=<your_openai_api_base_url>
    ```

## 使用方法

### 运行ReAct代理

1. 进入项目目录，运行以下命令启动ReAct代理：
    ```bash
    python react_agent.py
    ```


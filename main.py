from react_agent import ReactAgent


if __name__ == "__main__":
    agent = ReactAgent(model="qwen-max")

    agent.run("黑神话悟空至今盈利了多少？", extra_requirements="请你用文言文回答")

from pydantic import BaseModel, Field


class Message(BaseModel):
    """
    Represents a message with sender role and content.
    """
    role: str = Field(..., description="The role of the message sender.")
    content: str = Field(..., description="The content of the message.")


if __name__ == '__main__':
    history = [Message(role='user', content='保密法第三条和第四条有什么区别？'), Message(role='system', content='Final Answer: 保密法第三条强调了中国共产党对保密工作的领导，并说明了中央保密工作领导机构的职责，包括研究制定、指导实施国家保密工作战略和重大方针政策等。而第四条则概述了保密工作应遵循的基本原则，如坚持总体国家安全观、依法管理、积极防范等，并指出在确保国家秘密安全的同时也要便利信息资源的合理利用。这两条分别从领导机制和基本原则两个不同角度对保密工作进行了规定。')]

    print(history[-6:])

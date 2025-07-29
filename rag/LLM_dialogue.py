import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from app.logger import logger

from dotenv import load_dotenv
load_dotenv()

class LLMDialogue:
    """大语言模型对话类."""

    def __init__(self, history_store):
        """初始化LLMDialogue类的实例.

        Args:
            history_store(dict,optional):会话历史储存.
        """
        self.history_store = history_store or {}  # 使用main传入的存储

        self.system_prompt = """
        作为多领域专家系统，执行以下协议：

        1. 角色自适配：
            - 编程→代码生成器（自动语法校验）
            - 数学→定理证明器(附带Lean4验证)
            - 医学→诊断引擎(WHO标准)
            - 其他领域→对应专业终端

        2. 直接输出规范：
           技术问题：最优解 + 验证通过的可执行代码 
           学术问题:已发表的实验方案(DOI编号)
           生活决策:临床验证建议(FDA等级标注)

        3. 安全协议激活：
           !if 检测到[政治/伦理/暴力]模式：
              触发三重过滤→输出"该领域超出服务范围"

        4. 置信保障：
           ≥85%可信结论直接输出
           <85%可信度时→精确指明缺失参数

        （系统状态：结论模式激活） """

        self.model = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
            model=os.getenv("OPENAI_MODEL")
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="history"),  # 动态历史消息插槽
            ("human", "{input}"),
        ])

        # 构建处理流水线
        self.chain = self.prompt | self.model

        # 多会话记忆存储
        self.history_store = history_store or {}

    def chat(self, user_input, session_id):
        """执行对话处理.

        Args:
            user_input: 用户指令.
            session_id: 会话唯一标识符.

        Returns:
            str: 模型生成响应内容.
        """
        # 会话记忆初始化
        if session_id not in self.history_store:
            logger.warning(f"会话{session_id}未初始化!")
            return "会话错误：请重新开始会话"

        # 获取当前会话的历史
        history = self.history_store[session_id]

        # 构建带有历史上下文的执行链
        chain_with_history = RunnableWithMessageHistory(
            self.chain,
            lambda _: history,  # 确保访问的是当前会话的历史
            input_messages_key="input",
            history_messages_key="history"
        )

        response = chain_with_history.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )

        return response.content


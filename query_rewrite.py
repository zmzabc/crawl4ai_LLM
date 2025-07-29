from openai import OpenAI
import os
from app.logger import logger
from dotenv import load_dotenv

load_dotenv()

class QueryRewrite:
    """用于重写用户当前问题，使其在对话中独立、完整、精炼。

    该类调用 deepseek 的对话模型，根据上一轮问答内容，将当前用户的问题改写成自洽的问题。
    """

    def __init__(self, last_question, last_answer, current_question):
        """
        初始化 QueryRewrite 实例。

        Args:
            last_question (str): 上一个用户问题。
            last_answer (str): 对应的 AI 回答。
            current_question (str): 当前用户的问题（需被重写）。
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL")
        self.model = os.getenv("OPENAI_MODEL")
        self.last_question = last_question
        self.last_answer = last_answer
        self.current_question = current_question

    def rewrite(self):
        """
        调用大语言模型将当前问题重写为独立、完整、简洁的问题。

        Returns:
            str: 重写后的问题文本。
        """
        client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

        prompt = f"""
你是一个对话理解专家。请根据上一轮问答内容，将用户当前问题重写为一个完整、自洽、独立的问题。

上一个问题：{self.last_question}
AI 的回答：{self.last_answer}
当前问题：{self.current_question}

请重写当前问题，使其不依赖上下文，表意清晰简洁。
"""

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一个对话理解专家，请帮助重写用户的问题为独立、完整且精简的问题"},
                {"role": "user", "content": prompt}
            ],
        )

        result = response.choices[0].message.content.strip()
        logger.debug(f"重写后的问题为: {result}")
        return result
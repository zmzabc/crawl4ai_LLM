import os
from langchain.embeddings import JinaEmbeddings
from dotenv import load_dotenv
load_dotenv()
from app.logger import logger

class PDFEmbedding:
    """基于Jina Embeddings API生成文本向量的类.

    该类用于加载远程的Jina模型,以便后续进行相似性计算.
    """

    def __init__(self, model_name='jina-embeddings-v4'):
        """初始化PDFEmbedding类,加载Jina嵌入模型.

        Args:
            model_name(str):Jina嵌入模型名称.

        Raises:
            Exception: 如果模型加载失败，将捕获异常并记录错误日志。
        """
        try:
            self.embeddings = JinaEmbeddings(
                model_name = model_name,
                jina_api_key=os.getenv("JINA_API_KEY"),
        )
            
        except Exception as e:
            logger.error(f"模型加载失败:{e}")
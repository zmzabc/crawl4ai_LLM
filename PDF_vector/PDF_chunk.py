import os
from langchain.document_loaders import PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.logger import logger

class PDFChunk:
    """实现PDF加载和文本分块功能的类.

    该类负责加载PDF文件并将其分割成多个文本块.
    """

    def __init__(self,pdf_path):
        """初始化PDF处理实例.

        Args:
            pdf_path(str):PDF文件路径.
        """
        if not os.path.isfile(pdf_path):
            logger.error(f"提供的PDF路径无效: {pdf_path}")
            
        self.pdf_path = pdf_path

    def read_and_split(self,chunk_size =1000):
        """执行PDF加载和文本分块.

        Args:
            chunk_size(int):文本块长度.

        Returns:
            list:分割后的文档列表,如果发生错误则返回空列表.
        """
        try:
            loader = PDFPlumberLoader(file_path=self.pdf_path, extract_images=False)
            documents = loader.load()

            logger.debug(f"加载的文档数量: {len(documents)}")
            splitter=RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_size // 10  # 根据要求调整重叠
            )
            split_docs = splitter.split_documents(documents)

            logger.debug(f"分割后的文档数量: {len(split_docs)}")
            return split_docs
        
        except Exception as e:
            logger.error(f"读取分割PDF出错:{self.pdf_path}:{e}")
            return []
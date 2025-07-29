import os
from app.logger import logger
from pinecone import Pinecone
from dotenv import load_dotenv
load_dotenv()

class QueryRerank:
    """结果重排序的类,用于根据查询文本得到的片段进行重新排序."""

    def __init__(self,query,retrieve_chunks,top_n = 5):
        """初始化QueryRerank实例.

        Args:
            query(str):用户查询文本.
            retrieve_chunks(list):需要重新排序的片段.
            top_n(int,optional):最多返回的重排序文档数量.
        """
        self.retrieve_chunks = retrieve_chunks
        self.query = query
        self.top_n = top_n

    def rerank(self):
        """执行基于语义的文档片段重排序，调用 Pinecone Rerank API.

        Returns:
            List[str]: 返回重排序后得分大于等于0.5的片段文本列表. 如果无有效片段，返回空列表.
        """
        index = 0
        rerank_docs = []
        for doc in self.retrieve_chunks:
            if doc.page_content and index <100:
                rerank_docs.append({"id":index,"text":doc.page_content})
                index += 1
        
        if not rerank_docs:
            logger.debug("未找到相关资讯")
            return rerank_docs
        
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        pc = Pinecone(api_key = pinecone_api_key)
        reranded_documents = pc.inference.rerank(
            model = "bge-reranker-v2-m3",
            query = self.query,
            documents = rerank_docs,
            top_n = self.top_n,
            return_documents = True
        )

        logger.debug(f"重排结果:\n{reranded_documents.rerank_result}")

        result_docs = []
        for rec in reranded_documents.rerank_result.data:
            if rec.score>=0.5:
                result_docs.append(rec.document.text)

        logger.info(f"重排返回的片段数为:{len(result_docs)}")
        logger.debug(f"分数大于0.5的结果:{result_docs}")
        return result_docs
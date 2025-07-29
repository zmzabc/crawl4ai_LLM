from langchain_chroma import Chroma
from app.logger import logger
from PDF_vector.PDF_embedding import PDFEmbedding

class QueryRetrieve:
    """向量召回类,用于执行基于向量的相似度检索."""

    def __init__(self,embedder,query):
        """初始化向量检索的实例.

        Args:
            embedder(PDFEmbedding):嵌入生成器实例.
            query(str):用户问题.
        """
        self.query = query
        self.embedder = embedder
        self.chroma_db = Chroma(collection_name="document_embeddings",
                                persist_directory='D:/Work/test_work/PDF_vector/chroma_embedding',
                                embedding_function=self.embedder.embeddings
                        )
        
    def query_vector(self,top_k=10):
        """执行向量相似度检索.

        Args:
            top_k(int,optional):需要返回的结果数.

        Returns:
            list:返回与查询最相似的文档内容列表.如果检索失败则返回空列表.
        """
        try:
            results = self.chroma_db.similarity_search(self.query, k=top_k)
            logger.debug(f"向量召回成功,共找到{len(results)}个文档")
            logger.debug(f"召回片段为:{results}")
            return results
        
        except Exception as e:
            logger.error(f"向量召回失败:{e}")
            return []
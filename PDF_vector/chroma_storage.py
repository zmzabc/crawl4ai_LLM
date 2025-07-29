from langchain_chroma import Chroma 
from app.logger import logger
from PDF_vector.PDF_embedding import PDFEmbedding
import uuid

class ChromaStorage:
    """用于管理Chroma向量库存储的类.

    该类负责初始化Chroma向量存储并提供文档嵌入功能.
    """

    def __init__(self,embedder):
        """初始化Chroma存储实例.

        Args:
            embedder(PDFEmbedding):嵌入生成器实例.
        """
        self.embedder = embedder
        self.persist_directory = 'D:/Work/test_work/PDF_vector/chroma_embedding'
        self.vector_store = Chroma(collection_name="document_embeddings", #集合名称
                                   embedding_function=self.embedder.embeddings,  #嵌入生成函数
                                   persist_directory=self.persist_directory
                                   )
        
    def add_embeddings(self, documents,batch_size=512):
        """将文档嵌入添加到向量数据库中.

        Args:
            documents(list):包含文档内容的列表,每个文档包含metadata属性.
        """
        try:
            for doc in documents:
                # 检查文档是否已有唯一ID，如果没有则生成一个新的UUID
                if "doc_id" not in doc.metadata:
                    doc.metadata["doc_id"] = str(uuid.uuid4())
            
            for i in range(0,len(documents),batch_size):
                batch_docs = documents[i:i + batch_size]
                self.vector_store.add_documents(documents=batch_docs)
                logger.debug(f"成功添加第 {i//batch_size + 1} 批向量, 数量: {len(batch_docs)}")
                
            logger.debug(f"添加向量库成功")
            
        except Exception as e:
            logger.error(f"添加向量库失败:{e}")
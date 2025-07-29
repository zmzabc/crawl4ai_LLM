from PDF_vector.PDF_chunk import PDFChunk
from PDF_vector.chroma_storage import ChromaStorage
from PDF_vector.PDF_embedding import PDFEmbedding

class SinglePDFProcess:
    """处理单个文件的类."""

    def __init__(self,pdf_path):
        """初始化SinglePDFProcess类的实例.

        Args:
            pdf_path(str):PDF文件的路径.
        """
        self.pdf_path = pdf_path

    def process(self):
        """处理单个PDF文件并将其嵌入到存储中.

        Raises:
            Exception:如果处理过程中发生错误将抛出异常
        """
        pdf_chunk = PDFChunk(self.pdf_path)
        embedder = PDFEmbedding()
        chroma_storage = ChromaStorage(embedder)

        split_documents = pdf_chunk.read_and_split()
        chroma_storage.add_embeddings(split_documents)
from PDF_vector.single_PDF_process import SinglePDFProcess
from document_check import DocumentCheck
from app.logger import logger
import os

def main():
    """PDF处理主程序.

    该函数遍历指定目录的公司文件夹,查找PDF并进行处理.
    """
    directory = 'D:/Work/test_work/documents/'

    documentcheck = DocumentCheck(directory)

    for company,folder_path in documentcheck.check():
        pdf_files = [f for f in os.listdir(folder_path)
                     if f.lower().endswith('.pdf')]

        if not pdf_files:
            logger.info(f"公司目录无PDF文件:{company}")

        for pdf_file in pdf_files:
            pdf_path = os.path.join(folder_path, pdf_file)
            try:
                singlePDFprocess = SinglePDFProcess(pdf_path)
                singlePDFprocess.process()
            except Exception as e:
                logger.error(f"处理PDF失败:{pdf_path},错误:{e}")

if __name__ == "__main__":
    main()
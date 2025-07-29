from setting.settings import COMPANY_MAP
from app.logger import logger
import os

class DocumentCheck:
    """检查指定目录中公司文件夹的存在性."""

    def __init__(self,directory):
        """初始化DocumentCheck类的实例.

        Args:
            directory(str):要检查的目录路径.
        """
        self.directory = directory
        self.companies = [company for company in COMPANY_MAP]
    
    def check(self):
        """检查每个公司文件夹是否存在于指定目录中.

        生成器方法,逐个返回存在的公司以及其对应的目录.
        """
        for company in self.companies:
            company_dir = os.path.join(self.directory, company)
            if os.path.isdir(company_dir):
                yield company,company_dir
            else:
                logger.debug(f"跳过不存在的公司:{company}")
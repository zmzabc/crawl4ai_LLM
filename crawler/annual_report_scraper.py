import os
from crawl4ai import *
from app.logger import logger

from crawler.extract_pdfs_url import ExtractPDFsUrl
from setting.settings import COMPANY_MAP
from crawler.base_scraper import BaseScraper
from crawler.download_pdf import Download_PDF

class AnnualReportScraper(BaseScraper):
    """年度报告爬取器."""

    def __init__(self,company,year):
        """初始化年度报告爬取器.

        Args:
            company(str):公司名称.
            year(int):目标年份.
        """
        super().__init__()
        self.company = company
        self.year = year
        self.folder = f"D:/Work/test_work/documents/{company}"
        os.makedirs(self.folder, exist_ok=True)

    async def fetch_report(self):
        """主爬取流程控制.

        负责控制整个爬取流程,包括获取公司基本URL,执行爬虫并下载PDF文件.
        """
        base_url = COMPANY_MAP.get(self.company)
        if not base_url:
            logger.error(f"公司{self.company}不存在")
            return
        
        async with AsyncWebCrawler(config = self.browser_config) as crawler:
            try:
                results = await crawler.arun(
                    url = base_url,
                    bypass_cache = True,
                    config = self.crawler_config
                )
            except Exception as e:
                logger.error(f"爬虫执行失败:{e}")

            extract_url = ExtractPDFsUrl(results.markdown,self.year)
            pdfs_url = await extract_url.extract()
            
            downloadpdf = Download_PDF(pdfs_url,self.folder)
            await downloadpdf.download_pdfs()

        logger.info("下载内容完成")
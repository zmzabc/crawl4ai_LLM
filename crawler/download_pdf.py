import aiofiles
import aiohttp
import asyncio
from app.logger import logger
from crawler.base_scraper import BaseScraper
import os

class Download_PDF(BaseScraper):
    """下载PDF文件的类.

    该类用于批量下载指定URL列表中的PDF文件,并将其保存到指定文件夹中.
    """

    def __init__(self,pdfs_urls,folder):
        """初始化Download_PDF类的实例.

        Args:
            pdfs_urls(list):包含PDF文件URL的列表.
            folder(str):下载保存的文件夹路径.
        """
        super().__init__()
        self.pdfs_urls = pdfs_urls
        self.folder = folder
        
    async def download_pdfs(self):
        """批量下载PDF文件."""
        download_tasks = [self.download_single_pdf(url,self.folder) 
                          for url in self.pdfs_urls]
        await asyncio.gather(*download_tasks)

    async def download_single_pdf(self, url, folder):
        """单个PDF文件下载.

        Args:
            url(str):PDF文件的URL.
            folder(str):下载保存的文件夹路径.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=30) as response:
                    if response.status != 200:
                        logger.error(f"下载失败:{url},状态码：{response.status}")
                        return

                    filename = url.split('/')[-1]  
                    filepath = os.path.join(folder,filename)

                    content = await response.read()
                    async with aiofiles.open(filepath,"wb") as f:
                        await f.write(content)

                logger.debug(f"下载成功:{filename}")
                return

        except Exception as e:
            logger.error(f"下载出错:{e}")
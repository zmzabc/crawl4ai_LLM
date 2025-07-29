from openai import OpenAI
from abc import ABC
import os
from crawl4ai import *
from dotenv import load_dotenv
load_dotenv()

class BaseScraper(ABC):
    """网页爬取基类(抽象类).

    该类定义了网页爬虫的基本结构和初始化方法.
    """

    def __init__(self):
        """初始化爬虫实例."""
        self.browser_config = BrowserConfig(
            headless=True
        )

        self.crawler_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS
        )
        
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )
        self.model = os.getenv("OPENAI_MODEL")

        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0'
            }
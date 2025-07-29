import sys
import asyncio
from crawler.annual_report_scraper import AnnualReportScraper

async def main():
    """异步主函数，执行爬取任务.
    
    该函数创建一个AnnualReportScraper实例,并调用fetch_report方法来爬取年报.
    """
    scraper = AnnualReportScraper(company= sys.argv[1],year = sys.argv[2])
    await scraper.fetch_report()

if __name__ == '__main__':
    asyncio.run(main())
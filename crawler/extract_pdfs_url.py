from app.logger import logger
from crawler.base_scraper import BaseScraper

class ExtractPDFsUrl(BaseScraper):
    """从Markdown内容中提取PDF链接的类."""

    def __init__(self,markdown,year):
        """初始化ExtractPDFsUrl类的实例.

        Args:
            markdown(str):网页的markdown内容.
            year(int):目标年份,用于筛选年报.
        """
        super().__init__()
        self.year = year
        self.markdown = markdown

    async def extract(self):
        """使用大模型分析提取PDF链接.

        Returns:
            list:提取到的PDF链接列表.如没有匹配链接则返回空列表.
        """
        prompt = f""" 
    你是一个专业的网页内容分析助手。你的任务是从给定的网页Markdown内容中精准提取目标年份的年度报告PDF链接,请严格遵循以下规则:

    1. 核心筛选标准:
       - 仅提取包含 明确年度报告标识 的PDF链接
       - 中文标识："年度报告"、"年报"(排除"半年度"、"季度")
       - 英文标识："Annual Report"(排除"Interim"/"Quarterly")
       - 文件扩展名必须是 .pdf

    2. 年份精准匹配:
     - 必须包含{self.year}年标识:
       - 数字格式:2024、'24
       - 中文格式:2024年、二零二四
       - 英文格式:2024、FY2024
       - 接受相邻字符组合(如"2024年报"、"AnnualReport2024")

    3. 严格排除规则:
     - 排除包含以下关键词的链接：
       - 财务报告(Financial Report)
       - 投资者报告(Investor Report)
       - ESG/社会责任报告
       - 审计报告(Audit Report)
       - 临时公告/简报
     - 排除非年度报告文件(即使含2024)

    4. 链接处理:
       - 保留原始URL格式(绝对/相对路径)
       - 仅返回 纯URL (无标题/描述文本)
       - 多个有效链接用英文逗号分隔
       - 无匹配时返回空字符串

    示例有效链接：
    /2024_Annual_Report.pdf
    https://example.com/年报2024.pdf
    docs/FY2024_Annual-Report_final.pdf

    示例无效链接（应排除）：
    2024_Financial_Statements.pdf  ← 财务报告非年报
    Q4_2024_Investor_Update.pdf   ← 投资者报告
    Sustainability_Report_2024.pdf ← ESG报告
    """
        
        messages = [
            {"role":"system","content":prompt},
            {"role":"user","content":f"目标年份:{self.year},markdown内容:{self.markdown}"}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False,
                temperature=0.7
            )

            response_content = response.choices[0].message.content
            logger.debug(f"大模型处理结果:{response_content}")

            if response_content.strip() == "":
                logger.info("未提取到任何PDF链接")
                return []
            
            urls =  [url.strip() for url in response_content.split(",") if url.strip()]
            logger.info(f"提取到的PDF链接:{urls}")
            return urls
            
        except Exception as e:
            logger.error(f"大模型分析失败:{e}")
            return []
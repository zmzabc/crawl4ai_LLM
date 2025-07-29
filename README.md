# Crawl4ai_LLM System

## 项目简介

本项目旨在构建一个基于大型语言模型（LLM）的检索增强生成（RAG）系统，专注于从上市公司年报中提取信息并进行智能问答。系统集成了网络爬虫、PDF文档处理、向量嵌入以及多轮对话管理等功能，旨在为用户提供高效、准确的年报信息检索与交互体验。通过自动化年报的获取、解析和知识库构建，本系统能够显著提升对海量非结构化文档的理解和利用效率，为金融分析、市场研究等领域提供强有力的支持。




## 项目结构

```
LLM_project/
├── LLM/
│   ├── PDF_vector/             # PDF文档向量化处理模块
│   │   ├── chroma_embedding/   # ChromaDB嵌入存储相关文件
│   │   ├── PDF_chunk.py        # PDF文档分块处理逻辑
│   │   ├── PDF_embedding.py    # PDF文档嵌入生成逻辑 (基于Jina Embeddings)
│   │   └── single_PDF_process.py # 单个PDF文档处理流程
│   ├── crawler/                # 网络爬虫模块
│   │   ├── annual_report_scraper.py # 年报爬取器，负责爬取公司年报
│   │   ├── base_scraper.py     # 爬虫基类
│   │   ├── download_pdf.py     # PDF文件下载逻辑
│   │   └── extract_pdfs_url.py # 从网页中提取PDF链接
│   ├── documents/              # 存储下载的年报PDF文件
│   ├── rag/                    # 检索增强生成 (RAG) 模块
│   │   ├── LLM_dialogue.py     # LLM对话管理逻辑
│   │   ├── query_rerank.py     # 查询结果重排逻辑
│   │   └── query_retrieve.py   # 查询检索逻辑
│   ├── setting/                # 项目配置模块
│   │   └── settings.py         # 存储公司映射等配置信息
│   ├── app/                    # 应用相关模块 (例如日志)
│   │   └── logger.py           # 日志配置
│   ├── crawl_main.py           # 爬虫主入口文件
│   ├── document_check.py       # 文档检查工具
│   ├── query_rewrite.py        # 查询重写逻辑 (用于多轮对话)
│   ├── rag_main.py             # RAG系统主入口文件
│   ├── vector_main.py          # 向量化主入口文件
│   └── README.md               # 项目说明文件
```




## 主要功能

- **年报自动化爬取**: 通过 `crawl_main.py` 脚本，可以指定公司和年份，自动从指定网站爬取并下载对应的上市公司年报PDF文件。支持多公司、多年份的灵活配置。
- **PDF文档处理与向量化**: `PDF_vector` 模块负责将下载的PDF文档进行分块（`PDF_chunk.py`），并利用Jina Embeddings（`PDF_embedding.py`）生成高质量的向量嵌入。这些向量存储在ChromaDB中，为后续的检索提供基础。
- **智能检索增强生成 (RAG)**: `rag_main.py` 是RAG系统的核心入口。它结合了以下功能：
  - **查询重写**: `query_rewrite.py` 实现了多轮对话中的查询重写功能，确保在上下文丢失的情况下，用户的问题依然能够被准确理解。
  - **向量检索**: `query_retrieve.py` 根据用户查询，从向量数据库中检索最相关的文档块。
  - **结果重排**: `query_rerank.py` 对检索到的文档块进行二次排序，以提高相关性。
  - **LLM对话**: `LLM_dialogue.py` 负责与大型语言模型进行交互，结合检索到的信息生成准确、流畅的回答。
- **会话管理**: 系统支持多会话管理，每个会话都有独立的聊天历史和上下文，确保对话的连贯性。
- **可配置性**: 通过 `setting/settings.py` 文件，可以方便地配置公司映射等参数，以适应不同的爬取需求。




## 安装指南

### 环境要求

- Python 3.8+
- pip

### 依赖安装

1. 克隆项目仓库：

   ```bash
   git clone <your-repository-url>
   cd LLM
   ```

2. 安装项目依赖：

   ```bash
   pip install -r requirements.txt
   ```

   **注意**：`requirements.txt` 文件未在提供的压缩包中，请根据项目实际使用的库手动创建此文件。以下是一些可能需要的库：

   - `crawl4ai`
   - `langchain`
   - `langchain-community`
   - `python-dotenv`
   - `chromadb`
   - `unstructured` (用于PDF解析)
   - `tiktoken`
   - `loguru` (如果 `app/logger.py` 使用)

3. 配置API Key：

   本项目使用Jina Embeddings API。请在项目根目录下创建 `.env` 文件，并添加您的Jina API Key：

   ```
   JINA_API_KEY=your_jina_api_key_here
   ```

   同时，如果使用其他LLM服务，也请在此文件中配置相应的API Key。




## 使用指南

### 1. 爬取年报

运行 `crawl_main.py` 脚本来爬取指定公司和年份的年报。例如，爬取“腾讯”公司2023年的年报：

```bash
python crawl_main.py 腾讯 2023
```

爬取到的PDF文件将存储在 `documents/` 目录下。

### 2. PDF文档向量化

在进行RAG问答之前，需要将下载的PDF文档进行向量化处理。运行 `vector_main.py` 脚本：

```bash
python vector_main.py
```

该脚本会遍历 `documents/` 目录下的所有PDF文件，对其进行分块、嵌入并存储到ChromaDB中。

### 3. 启动RAG对话系统

运行 `rag_main.py` 脚本来启动RAG对话系统：

```bash
python rag_main.py
```

系统会提示您输入会话ID。您可以输入一个ID来开始新会话或切换到现有会话。在对话过程中，您可以输入问题，系统将结合年报内容为您提供答案。输入 `exit` 退出对话，输入 `切换会话` 更换会话。

**示例对话流程：**

```
请输入本次会话ID (默认: default_session): my_session_1

对话开始 (输入 'exit' 退出，'切换会话' 更换会话)

你: 腾讯2023年的营收是多少？
AI: 根据腾讯2023年年报，其总营收为xxx亿元人民币。

你: 净利润呢？
AI: 2023年腾讯的净利润为xxx亿元人民币。

你: 切换会话
请输入要切换的会话ID: new_session
已切换至会话：new_session

你: 阿里巴巴2022年的研发投入是多少？
AI: 很抱歉，当前资料不足，无法回答该问题。（如果未爬取阿里巴巴的年报）
```



## 联系方式

如果您有任何问题或建议，请通过以下方式联系我：

-   **邮箱**:zdeqetdrbagc@outlook.com
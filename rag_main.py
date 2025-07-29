from rag.query_rerank import QueryRerank
from rag.query_retrieve import QueryRetrieve
from langchain_community.chat_message_histories import ChatMessageHistory
from PDF_vector.PDF_embedding import PDFEmbedding
from rag.LLM_dialogue import LLMDialogue
from query_rewrite import QueryRewrite
from app.logger import logger


def init_session(session_id, history_store, context_store):
    """初始化一个新的会话历史和上下文信息。

    Args:
        session_id (str): 会话的唯一标识符。
        history_store (dict): 所有会话历史记录的字典。
        context_store (dict): 所有会话上下文（如上轮问答）的字典。
    """
    history_store.setdefault(session_id, ChatMessageHistory())
    context_store.setdefault(session_id, {"last_q": "", "last_a": ""})


def auto_rewrite(query, context):
    """根据上下文自动重写当前用户提问，使其具备独立性。

    如果存在上一轮的问题和回答，则调用 QueryRewrite 模型对当前问题进行上下文消融的改写。

    Args:
        query (str): 当前用户输入的问题。
        context (dict): 当前会话上下文，包括上一次的提问与回答。

    Returns:
        str: 改写后的用户问题。如果改写失败，则返回原始问题。
    """
    if context["last_q"] and context["last_a"]:
        try:
            return QueryRewrite(context["last_q"], context["last_a"], query).rewrite()
        except Exception as e:
            logger.warning(f"问题重写失败: {e}")
    return query


def main():
    """运行一个支持上下文和自动重写的多轮对话系统。"""
    embedder = PDFEmbedding()
    history_store, context_store = {}, {}

    session_id = input("请输入本次会话ID (默认: default_session): ") or "default_session"
    init_session(session_id, history_store, context_store)

    agent = LLMDialogue(history_store=history_store)
    print("\n对话开始 (输入 'exit' 退出，'切换会话' 更换会话)")

    while True:
        user_input = input("\n你: ").strip()

        if user_input == "exit":
            print("对话结束。")
            break

        elif user_input == "切换会话":
            session_id = input("请输入要切换的会话ID: ").strip() or "default_session"
            init_session(session_id, history_store, context_store)
            print(f"已切换至会话：{session_id}")

        else:
            try:
                ctx = context_store[session_id]
                query = auto_rewrite(user_input, ctx)

                chunks = QueryRetrieve(embedder, query).query_vector()
                reranked = QueryRerank(query, chunks).rerank()
                valid_chunks = [str(c) for c in reranked if c]

                if not valid_chunks:
                    print("AI: 很抱歉，当前资料不足，无法回答该问题。")
                    continue

                prompt = "\n\n".join(valid_chunks) + "\n\n" + query
                response = agent.chat(prompt, session_id)
                print(f"AI: {response}")

                ctx.update({"last_q": query, "last_a": response})

            except Exception as e:
                logger.error(f"出错了: {e}")
                print(f"出错了: {e}")


if __name__ == "__main__":
    main()
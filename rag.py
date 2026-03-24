from llm import query_llm


def generate_answer(vector_store, question: str, history=None, k: int = 6, max_tokens: int = 800):
    docs = vector_store.similarity_search(question, k=k)

    def get_text(doc):
        if isinstance(doc, dict):
            return doc.get("page_content", "")
        return getattr(doc, "page_content", "")

    context_texts = [get_text(doc) for doc in docs if get_text(doc)]
    context = "\n\n".join(context_texts)

    history_segment = ""
    if history and isinstance(history, list):
        history_pairs = []
        for item in history[-8:]:
            role = item.get("role", "user") if isinstance(item, dict) else "user"
            content = item.get("content") if isinstance(item, dict) else str(item)
            history_pairs.append(f"{role.title()}: {content}")
        history_segment = "\n".join(history_pairs)

    prompt = f"""
You are a friendly, conversational assistant. Use the provided document context to answer the user query.

Instructions:
- Use the context below as the main source.
- Answer concisely and clearly.
- Provide about 500 words when appropriate.
- Keep a chat style response.

Context:
{context}

Conversation History:
{history_segment}

Question:
{question}
"""

    return query_llm(prompt, max_tokens=max_tokens)

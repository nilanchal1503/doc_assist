import requests
from utils import retrieval
from utils import validator


def answer_question(document_text, user_question, history=None):
    if not document_text.strip():
        return {
            "answer": "The document appears to be empty.",
            "justification": ""
        }

    chunks = retrieval.split_text(document_text)
    index, _, chunk_list = retrieval.build_faiss_index(chunks)
    top_chunks = retrieval.search_top_k(index, chunk_list, user_question, k=3)

    if not top_chunks:
        return {
            "answer": "Sorry, I couldn't find relevant content for your question.",
            "justification": ""
        }

    combined_context = " ".join(top_chunks)

    # Optional memory chaining using chat history
    chat_block = ""
    if history:
        for turn in history:
            chat_block += f"{turn['role'].capitalize()}: {turn['content']}\n"

    prompt = f"{chat_block}Context:\n{combined_context}\n\nQuestion: {user_question}\n\nAnswer:"

    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        result = response.json()

        if "choices" in result:
            answer = result["choices"][0]["message"]["content"].strip()

            # Optional: run plausibility check silently
            try:
                _ = validator.is_answer_plausible(answer, top_chunks)
            except Exception:
                pass  # Never let this interrupt response

            return {
                "answer": answer,
                "justification": top_chunks[0]
            }

        return {
            "answer": "❌ API did not return a valid response.",
            "justification": str(result)
        }

    except Exception as e:
        return {
            "answer": "⚠️ Something went wrong while fetching the answer.",
            "justification": str(e)
        }

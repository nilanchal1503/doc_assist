import requests

def generate_summary(text, max_words=150):
    if len(text.strip()) < 100:
        return "The document is too short to summarize."

    prompt = f"""Please summarize the following document clearly and concisely in about {max_words} words:

\"\"\"{text[:1500]}\"\"\"

Summary:"""

    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Error generating summary: {e}"

import requests
import json
import re
from utils import retrieval
from utils import validator


def generate_questions(document_text, num_questions=5):
    top_context = " ".join(retrieval.split_text(document_text)[:5])  # Use first few chunks

    prompt = f"""You're a teaching assistant.
From the following document excerpt, generate {num_questions} logic-based or comprehension-focused questions that test critical understanding.

Context:
\"\"\"{top_context}\"\"\"

Return them as a JSON list like:
["Question 1...", "Question 2...", "Question 3...", "Question 4...", "Question 5..."]
"""

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
        content = result["choices"][0]["message"]["content"].strip()

        # Try to parse JSON safely
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback: extract quoted questions manually
            rough_list = re.findall(r'"(.*?)"', content)
            return rough_list if rough_list else [f"⚠️ Failed to parse: {content}"]

    except Exception as e:
        return [f"❌ Question generation failed: {e}"]


def evaluate_answer(document_text, question, user_answer):
    relevant_chunks = retrieval.search_top_k(None, retrieval.split_text(document_text), question, k=3)
    context = " ".join(relevant_chunks)

    prompt = f"""You're an evaluator.
Given the document context and a user's answer to a question, assess the accuracy logically and provide feedback with justification.

Context:
\"\"\"{context}\"\"\"

Question: {question}
User Answer: {user_answer}

Respond like:
Feedback: <Good/Okay/Incorrect>
Explanation: <short explanation>
"""

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
        feedback = result["choices"][0]["message"]["content"].strip()

        valid, _ = validator.is_answer_plausible(feedback, relevant_chunks)
        if not valid:
            feedback += "\n\n⚠️ SanityCheck: This feedback may not fully reflect the document."

        return feedback

    except Exception as e:
        return f"⚠️ Evaluation failed: {e}"


__all__ = ["generate_questions", "evaluate_answer"]

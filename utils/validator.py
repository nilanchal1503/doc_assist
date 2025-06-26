import difflib

def is_empty_response(response_text):
    """
    Checks if the model response is empty or suggests uncertainty.
    """
    return len(response_text.strip()) == 0 or "i'm not sure" in response_text.lower()

def relevance_score(response, context):
    """
    Calculates similarity ratio between response and context using difflib.
    """
    return difflib.SequenceMatcher(None, response.lower(), context.lower()).ratio()

def is_answer_plausible(answer, context_chunks, threshold=1):
    """
    Checks if the answer aligns well with the document chunks.
    Returns a boolean (validity) and the similarity score.
    """
    combined_context = " ".join(context_chunks)
    score = relevance_score(answer, combined_context)
    print(f"[DEBUG] Answer plausibility score: {score}")  
    return score >= threshold, score

import difflib

def split_text(text, chunk_size=300):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def search_top_k(index, chunk_list, question, k=3):
    ranked = sorted(
        chunk_list,
        key=lambda chunk: difflib.SequenceMatcher(None, question, chunk).ratio(),
        reverse=True
    )
    return ranked[:k]

def build_faiss_index(chunks):  # Dummy version now
    return None, None, chunks

import fitz  # PyMuPDF

def extract_text(file):
    if file.name.endswith(".pdf"):
        return _extract_from_pdf(file)
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        return ""

def _extract_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

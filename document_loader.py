from pypdf import PdfReader


def load_and_split(file_path: str):
    reader = PdfReader(file_path)
    text_pieces = []

    for page_num, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        text_pieces.append(f"[page {page_num}]\n{page_text}")

    full_text = "\n\n".join(text_pieces)

    chunk_size = 1500
    chunk_overlap = 250
    words = full_text.split()

    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_text = " ".join(words[start:end])
        chunks.append({"page_content": chunk_text, "metadata": {"source": file_path}})
        start += chunk_size - chunk_overlap

    return chunks

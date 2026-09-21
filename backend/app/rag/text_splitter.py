from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_pages(pages: list[dict], chunk_size: int, chunk_overlap: int) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap,
                                               separators=["\n\n", "\n", ". ", " ", ""])
    chunks = []
    for page in pages:
        for text in splitter.split_text(page["text"]):
            chunks.append({"text": text, "page": page["page"]})
    return chunks

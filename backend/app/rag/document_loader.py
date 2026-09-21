from pathlib import Path
import fitz


def load_pdf(path: Path) -> list[dict]:
    with fitz.open(path) as document:
        return [{"text": page.get_text("text").strip(), "page": number}
                for number, page in enumerate(document, start=1) if page.get_text("text").strip()]

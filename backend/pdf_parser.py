# backend/pdf_parser.py
import pdfplumber
from pathlib import Path
from docx import Document

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx", ".png", ".jpg", ".jpeg"}

def extract_text(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return _extract_from_pdf(file_path)
    elif ext == ".txt":
        return _extract_from_txt(file_path)
    elif ext == ".docx":
        return _extract_from_docx(file_path)
    elif ext in {".png", ".jpg", ".jpeg"}:
        return _extract_from_image(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def _extract_from_pdf(file_path: str) -> str:
    text_chunks = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)

    if text_chunks:
        return "\n".join(text_chunks)

    # Fallback to OCR if no text found (scanned PDF)
    return _ocr_pdf(file_path)

def _ocr_pdf(file_path: str) -> str:
    """Convert scanned PDF pages to images then OCR."""
    try:
        import pytesseract
        from pdf2image import convert_from_path
        pages = convert_from_path(file_path, dpi=200)
        texts = [pytesseract.image_to_string(p) for p in pages]
        result = "\n".join(texts).strip()
        if not result:
            raise ValueError("OCR returned no text from scanned PDF.")
        return result
    except ImportError:
        raise ValueError(
            "PDF appears to be scanned/image-based. "
            "Install pdf2image and pytesseract for OCR support."
        )

def _extract_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def _extract_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    if not paragraphs:
        raise ValueError("Could not extract any text from DOCX.")
    return "\n".join(paragraphs)

def _extract_from_image(file_path: str) -> str:
    """Direct OCR on uploaded image files."""
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img).strip()
        if not text:
            raise ValueError("OCR returned no text from image.")
        return text
    except ImportError:
        raise ValueError("Install pytesseract and Pillow for image OCR support.")
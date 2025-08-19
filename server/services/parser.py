import fitz  # PyMuPDF
import docx
import pytesseract
from PIL import Image
from unstructured.partition.auto import partition
import os


def parse_pdf(file_path: str) -> str:
    """Extract text from a PDF (non-scanned)."""
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text.strip()


def parse_docx(file_path: str) -> str:
    """Extract text from a Word document."""
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()


def parse_image(file_path: str) -> str:
    """Extract text from an image using OCR."""
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text.strip()


def parse_with_unstructured(file_path: str) -> str:
    """Fallback parser for multiple formats (PPT, HTML, etc.)."""
    elements = partition(filename=file_path)
    text = "\n".join([str(el) for el in elements])
    return text.strip()


def parse_document(file_path: str) -> str:
    """Main entry point: detect file type and parse accordingly."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        try:
            text = parse_pdf(file_path)
            if not text.strip():
                # If empty, try OCR
                return parse_image(file_path)
            return text
        except Exception:
            return parse_image(file_path)

    elif ext == ".docx":
        return parse_docx(file_path)

    elif ext in [".png", ".jpg", ".jpeg", ".tiff"]:
        return parse_image(file_path)

    else:
        # Fallback for other formats
        return parse_with_unstructured(file_path)
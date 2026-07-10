import io
from PyPDF2 import PdfReader


def extract_text_from_pdf(file_bytes: bytes)-> str:

    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text +=page.extract_text()
    return text.strip()

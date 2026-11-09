from io import BytesIO
from pathlib import Path

def extract_text_from_file(file_name: str, file_bytes: bytes) -> str:
    ext = Path(file_name).suffix.lower()
    if ext == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(BytesIO(file_bytes))
        text = "\n".join((page.extract_text() or "") for page in reader.pages).strip()
    elif ext == ".docx":
        from docx import Document
        doc = Document(BytesIO(file_bytes))
        parts = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                parts.append(" | ".join(cell.text.strip() for cell in row.cells))
        text = "\n".join(parts).strip()
    elif ext == ".txt":
        text = file_bytes.decode("utf-8", errors="ignore").strip()
    else:
        raise ValueError("Supported formats: PDF, DOCX, TXT.")
    if not text:
        raise ValueError("No readable text was found. A scanned/image-only PDF may need OCR.")
    return text

def basic_resume_sections(text: str) -> dict:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    low = text.lower()
    return {
        "line_count": len(lines),
        "character_count": len(text),
        "sections_detected": {
            "summary": any(k in low for k in ["summary", "profile", "objective"]),
            "education": "education" in low,
            "skills": "skills" in low,
            "experience": any(k in low for k in ["experience", "employment"]),
            "projects": "projects" in low,
            "certifications": any(k in low for k in ["certification", "certificate"]),
            "achievements": any(k in low for k in ["achievement", "awards"]),
        },
    }

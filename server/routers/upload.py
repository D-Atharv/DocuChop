from fastapi import APIRouter, UploadFile, File
import shutil
import os
from services.parser import parse_document

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse document into text
    text = parse_document(file_path)

    return {
        "filename": file.filename,
        "path": file_path,
        "extracted_text_preview": text[:500],  # return preview only
        "total_chars": len(text),
    }
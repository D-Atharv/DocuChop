from fastapi import APIRouter, UploadFile, File
import shutil
import os
from services.parser import parse_document
from services.embeddings import chunk_text, embed_chunks

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

    # Chunk text
    chunks = chunk_text(text, chunk_size=500, overlap=50)

    # Generate embeddings
    embeddings = embed_chunks(chunks)

    return {
        "filename": file.filename,
        "path": file_path,
        "num_chunks": len(chunks),
        "embedding_dim": len(embeddings[0]) if embeddings else 0,
        "sample_chunk": chunks[0] if chunks else "",
    }
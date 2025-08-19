from sentence_transformers import SentenceTransformer
from typing import List

# Load model once at startup
# all-MiniLM-L6-v2 is small, fast, and good for semantic search
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks.
    - chunk_size: number of words per chunk
    - overlap: number of words to overlap between chunks
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        start += chunk_size - overlap  # move forward with overlap

    return chunks


def embed_chunks(chunks: List[str]) -> List[List[float]]:
    """
    Generate embeddings for each chunk.
    Returns a list of vectors.
    """
    embeddings = embedding_model.encode(chunks, convert_to_numpy=True).tolist()
    return embeddings
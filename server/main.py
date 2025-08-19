from fastapi import FastAPI
from routers import upload, chat

app = FastAPI(title="AI Document Summarizer")

# Register routers
app.include_router(upload.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "AI Summarizer Backend is running 🚀"}
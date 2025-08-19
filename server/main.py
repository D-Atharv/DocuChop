from fastapi import FastAPI

app = FastAPI(title="AI Document Summarizer")

@app.get("/")
def root():
    return {"message": "AI Summarizer Backend is running 🚀"}
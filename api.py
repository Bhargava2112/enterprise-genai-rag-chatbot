"""FastAPI REST service. Install optional API dependencies to run."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.core import Retriever, answer

app = FastAPI(title="Enterprise Document Retrieval API", version="1.0.0")
retriever = Retriever()

class Document(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    text: str = Field(min_length=1, max_length=100000)

class Question(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(default=4, ge=1, le=20)

@app.get("/health")
def health():
    return {"status": "ok", "chunks": len(retriever.chunks)}

@app.post("/documents")
def ingest(doc: Document):
    count = retriever.add(doc.name, doc.text)
    if not count:
        raise HTTPException(status_code=422, detail="Document has no words")
    return {"name": doc.name, "chunks_added": count}

@app.post("/ask")
def ask(payload: Question):
    hits = retriever.search(payload.question, payload.top_k)
    return {**answer(payload.question, hits), "matches": hits}

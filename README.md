# Enterprise GenAI RAG Chatbot — Grounded Retrieval Starter

A working, testable **document retrieval API** with BM25-ranked text chunks and source citations. This initial version uses **extractive answers**, not a generative LLM: it deliberately avoids claiming generated responses or semantic embeddings. A production RAG model integration can be added behind a provider interface.

## Features
- Text document ingestion (`POST /documents`)
- Token-based BM25 search and ranked excerpts (`POST /ask`)
- Source citation labels and abstention on no match
- Configurable chunk overlap, input validation, health endpoint
- Automated tests and GitHub Actions CI

## Run
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -q
uvicorn app.api:app --reload
```
Visit `http://localhost:8000/docs` for interactive API documentation.

## Example
```bash
curl -X POST http://localhost:8000/documents -H 'Content-Type: application/json' -d '{"name":"aws.txt","text":"AWS Lambda runs serverless functions on demand."}'
curl -X POST http://localhost:8000/ask -H 'Content-Type: application/json' -d '{"question":"What runs serverless functions?"}'
```

## Limitations and next steps
- In-memory index resets on restart; add persistent database/storage.
- This is lexical retrieval, not vector embeddings or an LLM-generated answer.
- Add user authentication, document ownership, and access-control filtering before multi-tenant use.
- Add a configurable LLM, semantic retriever, retrieval evaluations, and prompt-injection safeguards before calling it a full generative RAG system.

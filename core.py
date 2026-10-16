"""Dependency-light, inspectable retrieval engine for local text documents."""
import math
import re
from collections import Counter
from pathlib import Path

TOKEN = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    return TOKEN.findall(text.lower())


class Retriever:
    def __init__(self):
        self.chunks: list[dict] = []

    def add(self, name: str, text: str, chunk_size: int = 180, overlap: int = 30) -> int:
        if not 0 <= overlap < chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")
        words = text.split()
        count = 0
        for start in range(0, len(words), chunk_size - overlap):
            part = words[start:start + chunk_size]
            if not part:
                break
            self.chunks.append({"source": name, "text": " ".join(part)})
            count += 1
            if start + chunk_size >= len(words):
                break
        return count

    def search(self, question: str, k: int = 4) -> list[dict]:
        q = tokenize(question)
        if not q or k < 1:
            return []
        documents = [tokenize(c["text"]) for c in self.chunks]
        n = len(documents)
        if not n:
            return []
        avg = sum(map(len, documents)) / n
        dfs = Counter(t for doc in documents for t in set(doc))
        results = []
        for chunk, tokens in zip(self.chunks, documents):
            freq = Counter(tokens)
            score = 0.0
            for term in set(q):
                if term not in freq:
                    continue
                idf = math.log(1 + (n - dfs[term] + 0.5) / (dfs[term] + 0.5))
                score += idf * freq[term] * 2.2 / (freq[term] + 1.2 * (0.25 + 0.75 * len(tokens) / avg))
            if score > 0:
                results.append({**chunk, "score": round(score, 4)})
        return sorted(results, key=lambda x: x["score"], reverse=True)[:k]


def answer(question: str, hits: list[dict]) -> dict:
    if not hits:
        return {"answer": "I couldn't find supporting evidence in the uploaded documents.", "citations": []}
    # Grounded extractive response: never fabricate model output or citations.
    excerpts = [h["text"][:350] for h in hits[:2]]
    return {"answer": "\n\n".join(excerpts), "citations": [h["source"] for h in hits[:2]]}


def load_directory(path: str) -> Retriever:
    engine = Retriever()
    for file in sorted(Path(path).glob("*.txt")):
        engine.add(file.name, file.read_text(encoding="utf-8"))
    return engine

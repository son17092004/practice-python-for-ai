"""Capstone Mini-Project: Mini Search Engine bằng Python thuần."""

import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Document:
    doc_id: str
    title: str
    text: str


def tokenize(text: str) -> list[str]:
    """Tách từ đơn giản: chuyển về chữ thường và chỉ giữ ký tự chữ/số."""
    return re.findall(r"[a-z0-9]+", text.lower())


def cosine_similarity(a: list[float], b: list[float]) -> float:
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / (norm_a * norm_b)


class TextVectorizer:
    """Chuyển đổi văn bản thành vector tần suất từ (Bag-of-Words / TF)."""

    def __init__(self):
        self.vocab: dict[str, int] = {}

    def fit(self, texts: list[str]) -> "TextVectorizer":
        unique_tokens = sorted(
            {tok for text in texts for tok in tokenize(text)}
        )
        self.vocab = {tok: idx for idx, tok in enumerate(unique_tokens)}
        return self

    def transform(self, text: str) -> list[float]:
        if not self.vocab:
            raise RuntimeError("Vectorizer chưa được fit() trên dữ liệu.")
        vec = [0.0] * len(self.vocab)
        counts = Counter(tokenize(text))
        total = sum(counts.values())
        if total == 0:
            return vec
        for tok, count in counts.items():
            if tok in self.vocab:
                vec[self.vocab[tok]] = count / total
        return vec


class MiniSearchEngine:
    """Bộ máy tìm kiếm tài liệu dựa trên Cosine Similarity."""

    def __init__(self, documents: list[Document]):
        self.documents = documents
        self.vectorizer = TextVectorizer().fit(
            [f"{d.title} {d.text}" for d in documents]
        )
        self.doc_vectors = [
            self.vectorizer.transform(f"{d.title} {d.text}") for d in documents
        ]

    def search(self, query: str, top_k: int = 3) -> list[tuple[Document, float]]:
        query_vec = self.vectorizer.transform(query)
        scored = [
            (doc, cosine_similarity(query_vec, doc_vec))
            for doc, doc_vec in zip(self.documents, self.doc_vectors)
        ]
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]


def load_corpus(path: Path) -> list[Document]:
    docs: list[Document] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                raw = json.loads(line)
                docs.append(
                    Document(doc_id=raw["id"], title=raw["title"], text=raw["text"])
                )
    return docs


if __name__ == "__main__":
    corpus_path = Path(__file__).parent / "corpus.jsonl"
    documents = load_corpus(corpus_path)
    engine = MiniSearchEngine(documents)

    queries = [
        "neural networks with tensors",
        "vector search and language models",
        "fast matrix linear algebra",
    ]
    for q in queries:
        print(f"\nQuery: '{q}'")
        for doc, score in engine.search(q, top_k=2):
            print(f"  [{score:.4f}] {doc.doc_id} - {doc.title}: {doc.text}")

"""Kiểm thử toàn bộ pipeline của Capstone Mini-Project."""

import math
from pathlib import Path

from main import MiniSearchEngine, load_corpus


def test_search_engine() -> None:
    corpus_path = Path(__file__).parent / "corpus.jsonl"
    docs = load_corpus(corpus_path)
    assert len(docs) == 5

    engine = MiniSearchEngine(docs)

    top_doc, score = engine.search("tensors and neural networks", top_k=1)[0]
    assert top_doc.doc_id == "doc1"
    assert score > 0.3

    top_rag, _ = engine.search("vector search language models", top_k=1)[0]
    assert top_rag.doc_id == "doc3"

    _, zero_score = engine.search("unrelatedxyzword", top_k=1)[0]
    assert math.isclose(zero_score, 0.0)

    print("Capstone Mini-Project: Tất cả bài test đã PASS!")


if __name__ == "__main__":
    test_search_engine()

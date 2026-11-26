"""Module 02: Lời giải tham khảo."""

import heapq
from collections import Counter
from itertools import cycle, islice
from typing import Iterable, Iterator


def build_vocab(sentences: list[str], min_freq: int = 1) -> dict[str, int]:
    counter = Counter(
        token for sent in sentences for token in sent.lower().split()
    )
    vocab = {"<pad>": 0, "<unk>": 1}
    valid_tokens = sorted(tok for tok, freq in counter.items() if freq >= min_freq)
    for idx, tok in enumerate(valid_tokens, start=2):
        vocab[tok] = idx
    return vocab


def encode_sentence(sentence: str, vocab: dict[str, int]) -> list[int]:
    unk_id = vocab["<unk>"]
    return [vocab.get(tok, unk_id) for tok in sentence.lower().split()]


def batch_generator(data: list, batch_size: int) -> Iterator[list]:
    if batch_size <= 0:
        raise ValueError("batch_size phải lớn hơn 0")
    for i in range(0, len(data), batch_size):
        yield data[i : i + batch_size]


def compute_accuracy(preds: list[int], labels: list[int]) -> float:
    if not labels:
        return 0.0
    correct = sum(p == y for p, y in zip(preds, labels))
    return correct / len(labels)


def top_k_documents(scores: dict[str, float], k: int) -> list[tuple[str, float]]:
    if k <= 0:
        return []
    return heapq.nlargest(k, scores.items(), key=lambda kv: kv[1])


def take_valid(stream: Iterable[str], n: int) -> list[str]:
    cleaned = (line.strip() for line in stream)
    return list(islice((line for line in cleaned if line), n))


def rank_words(text: str) -> list[str]:
    counts = Counter(text.lower().split())
    return sorted(counts, key=lambda w: (-counts[w], w))


if __name__ == "__main__":
    sentences = [
        "AI is the future",
        "Python is great for AI",
        "Learn Python for AI",
    ]
    vocab = build_vocab(sentences, min_freq=2)
    assert vocab == {"<pad>": 0, "<unk>": 1, "ai": 2, "for": 3, "is": 4, "python": 5}
    assert encode_sentence("Python and AI", vocab) == [5, 1, 2]
    assert list(batch_generator([1, 2, 3, 4, 5], batch_size=2)) == [[1, 2], [3, 4], [5]]
    assert compute_accuracy([1, 0, 1, 1], [1, 1, 1, 0]) == 0.5
    assert compute_accuracy([], []) == 0.0

    # Test 5: top_k_documents
    doc_scores = {"d1": 0.2, "d2": 0.9, "d3": 0.5, "d4": 0.7}
    assert top_k_documents(doc_scores, 2) == [("d2", 0.9), ("d4", 0.7)]
    assert top_k_documents(doc_scores, 10) == [("d2", 0.9), ("d4", 0.7), ("d3", 0.5), ("d1", 0.2)]
    assert top_k_documents(doc_scores, 0) == []

    # Test 6: take_valid (stream vô hạn -> nếu bạn gọi list(stream) chương trình sẽ treo!)
    infinite = cycle(["  hello ", "", "   ", "world", "\n"])
    assert take_valid(infinite, 3) == ["hello", "world", "hello"]
    assert take_valid(["a", " ", "b"], 5) == ["a", "b"]

    # Test 7: rank_words
    assert rank_words("b a c a b d") == ["a", "b", "c", "d"]
    assert rank_words("AI ai Python data python AI") == ["ai", "python", "data"]

    print("Module 02 (solutions): Tất cả bài test đã PASS!")

"""Module 02: Bài tập Cấu trúc dữ liệu & Comprehensions."""

import heapq
from collections import Counter, defaultdict
from itertools import cycle, islice
from typing import Iterable, Iterator


def build_vocab(sentences: list[str], min_freq: int = 1) -> dict[str, int]:
    """Xây dựng từ điển ánh xạ `token -> id` từ danh sách câu.

    Quy tắc:
    1. Chuyển câu về chữ thường và tách từ bằng `.split()`.
    2. Chỉ giữ các từ có tần suất >= `min_freq`.
    3. Gán id bắt đầu từ 2, sắp xếp các từ hợp lệ theo thứ tự bảng chữ cái (alphabetical).
    4. Luôn có 2 token đặc biệt ở đầu: {"<pad>": 0, "<unk>": 1}.
    """
    # TODO: Viết code tại đây
    flatted_words = [w for sen in sentences for w in sen.lower().split()]
    counts = dict(Counter(flatted_words))
    sorted_words = sorted([w for w,c in counts.items() if c >= min_freq])
    return {"<pad>":0, "<unk>": 1, **{w:i for i,w in enumerate(sorted_words, start=2)}}


def encode_sentence(sentence: str, vocab: dict[str, int]) -> list[int]:
    """Chuyển một câu thành danh sách token ID dựa trên `vocab`.

    Nếu từ không có trong `vocab`, dùng ID của `<unk>` (vocab["<unk>"]).
    """
    # TODO: Viết code tại đây
    return [vocab[w] if w in vocab else vocab["<unk>"] for w in sentence.lower().split()]


def batch_generator(data: list, batch_size: int) -> Iterator[list]:
    """Generator lần lượt yield các batch kích thước tối đa `batch_size` từ `data`.

    Gợi ý: Dùng `yield data[i : i + batch_size]`.
    Nếu `batch_size <= 0`, raise ValueError.
    """
    # TODO: Viết code tại đây
    if batch_size <= 0: 
        raise ValueError("batch_size must be > 0")
    for i in range(0, len(data), batch_size):
        yield data[i:i+batch_size]

def compute_accuracy(preds: list[int], labels: list[int]) -> float:
    """Tính độ chính xác (số dự đoán đúng / tổng số mẫu) bằng `zip` và generator.

    Nếu danh sách rỗng, trả về 0.0.
    """
    # TODO: Viết code tại đây
    len_preds = len(preds)
    if (len_preds == 0):
        return 0.0
    corrected= sum(1 for p,l in zip(preds, labels) if p==l)
    return corrected / len_preds


def top_k_documents(scores: dict[str, float], k: int) -> list[tuple[str, float]]:
    """Trả về k cặp (doc_id, score) có điểm CAO NHẤT, sắp xếp giảm dần theo score.

    Dùng `heapq.nlargest` (không sort toàn bộ). Nếu k <= 0 trả về [].
    Ví dụ: {"d1": 0.2, "d2": 0.9, "d3": 0.5}, k=2 -> [("d2", 0.9), ("d3", 0.5)]
    """
    # TODO: Viết code tại đây
    return heapq.nlargest(k, scores.items(), key=lambda x: x[1])

def take_valid(stream: Iterable[str], n: int) -> list[str]:
    """Lấy tối đa `n` dòng HỢP LỆ đầu tiên từ `stream` (có thể là iterator VÔ HẠN!).

    Dòng hợp lệ: sau khi `.strip()` không rỗng. Trả về các dòng đã được strip.
    Yêu cầu: KHÔNG được chuyển cả `stream` thành list (sẽ treo máy nếu stream vô hạn).
    Gợi ý: generator expression + `itertools.islice`.
    """
    # TODO: Viết code tại đây
    gen = (s.strip() for s in stream if s.strip())
    return list(islice(gen, n))


def rank_words(text: str) -> list[str]:
    """Trả về danh sách các từ KHÔNG trùng lặp (chữ thường, tách bằng `.split()`),
    sắp xếp theo:
    1. Tần suất GIẢM dần.
    2. Cùng tần suất thì theo bảng chữ cái a→z.

    Ví dụ: "b a c a b d" -> ["a", "b", "c", "d"]
    Gợi ý: `Counter` + `sorted(..., key=lambda w: (-counts[w], w))`.
    """
    # TODO: Viết code tại đây
    counts = Counter(text.lower().split())
    return sorted(counts.keys(), key = lambda w: (-counts[w],w ))


if __name__ == "__main__":
    sentences = [
        "AI is the future",
        "Python is great for AI",
        "Learn Python for AI",
    ]
    vocab = build_vocab(sentences, min_freq=2)
    assert vocab == {"<pad>": 0, "<unk>": 1, "ai": 2, "for": 3, "is": 4, "python": 5}

    assert encode_sentence("Python and AI", vocab) == [5, 1, 2]

    batches = list(batch_generator([1, 2, 3, 4, 5], batch_size=2))
    assert batches == [[1, 2], [3, 4], [5]]

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

    print("Module 02: Tất cả bài test đã PASS!")

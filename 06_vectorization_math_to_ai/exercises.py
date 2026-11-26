"""Module 06: Bài tập Toán học AI bằng Python thuần."""

import math


def dot_product(a: list[float], b: list[float]) -> float:
    """Tính tích vô hướng của 2 vector `a` và `b`.
    Nếu len(a) != len(b), raise ValueError.
    """
    # TODO: Viết code tại đây
    pass


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Tính Cosine Similarity giữa 2 vector `a` và `b`.
    Nếu một trong hai vector có chuẩn (norm) bằng 0, trả về 0.0.
    """
    # TODO: Viết code tại đây
    pass


def softmax(logits: list[float]) -> list[float]:
    """Tính Softmax với mẹo ổn định số học (trừ max(logits) trước khi tính math.exp).
    Nếu `logits` rỗng, trả về [].
    """
    # TODO: Viết code tại đây
    pass


def matmul(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    """Nhân 2 ma trận A (m x k) và B (k x n) -> kết quả (m x n).
    Nếu số cột của A != số dòng của B (hoặc ma trận rỗng), raise ValueError.
    """
    # TODO: Viết code tại đây
    pass


if __name__ == "__main__":
    # Test 1: dot_product
    assert dot_product([1.0, 2.0, 3.0], [4.0, -5.0, 6.0]) == 12.0

    # Test 2: cosine_similarity
    assert math.isclose(cosine_similarity([1.0, 0.0], [1.0, 0.0]), 1.0)
    assert math.isclose(cosine_similarity([1.0, 0.0], [0.0, 1.0]), 0.0)
    assert cosine_similarity([0.0, 0.0], [1.0, 2.0]) == 0.0

    # Test 3: softmax (kiểm tra cả trường hợp số lớn không bị OverflowError)
    probs = softmax([1000.0, 1001.0, 1000.0])
    assert math.isclose(sum(probs), 1.0, rel_tol=1e-6)
    assert probs[1] > probs[0] and math.isclose(probs[0], probs[2])

    # Test 4: matmul
    A = [[1, 2, 3], [4, 5, 6]]       # 2x3
    B = [[7, 8], [9, 10], [11, 12]]  # 3x2
    assert matmul(A, B) == [[58, 64], [139, 154]]

    print("Module 06: Tất cả bài test đã PASS!")

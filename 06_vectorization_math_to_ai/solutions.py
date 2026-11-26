"""Module 06: Lời giải tham khảo."""

import math


def dot_product(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Hai vector phải có cùng độ dài")
    return sum(x * y for x, y in zip(a, b))


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Hai vector phải có cùng độ dài")
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot_product(a, b) / (norm_a * norm_b)


def softmax(logits: list[float]) -> list[float]:
    if not logits:
        return []
    max_val = max(logits)
    exps = [math.exp(x - max_val) for x in logits]
    total = sum(exps)
    return [e / total for e in exps]


def matmul(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    if not A or not B or len(A[0]) != len(B):
        raise ValueError("Kích thước ma trận không hợp lệ để nhân")
    # Chuyển vị B (transpose) giúp nhân từng dòng với từng cột cực gọn bằng zip
    B_T = list(zip(*B))
    return [[dot_product(row_a, list(col_b)) for col_b in B_T] for row_a in A]


if __name__ == "__main__":
    assert dot_product([1.0, 2.0, 3.0], [4.0, -5.0, 6.0]) == 12.0
    assert math.isclose(cosine_similarity([1.0, 0.0], [1.0, 0.0]), 1.0)
    assert math.isclose(cosine_similarity([1.0, 0.0], [0.0, 1.0]), 0.0)
    assert cosine_similarity([0.0, 0.0], [1.0, 2.0]) == 0.0

    probs = softmax([1000.0, 1001.0, 1000.0])
    assert math.isclose(sum(probs), 1.0, rel_tol=1e-6)
    assert probs[1] > probs[0] and math.isclose(probs[0], probs[2])

    A = [[1, 2, 3], [4, 5, 6]]
    B = [[7, 8], [9, 10], [11, 12]]
    assert matmul(A, B) == [[58, 64], [139, 154]]

    print("Module 06 (solutions): Tất cả bài test đã PASS!")

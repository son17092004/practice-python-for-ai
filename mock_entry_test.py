"""Bài Test Thử Python Đầu Vào (20 câu hỏi trắc nghiệm & đọc hiểu code).

Chạy bằng lệnh:
    python3 mock_entry_test.py

Bao phủ các bẫy kinh điển: mutability, slicing, `is` vs `==`, tuple, scope,
closure late binding, generator, iterator, OOP class attribute, property,
try/except/else/finally, round(), match-case, regex, random.
"""

QUESTIONS = [
    {
        "q": """Câu 1: Kết quả của đoạn code sau là gì?
    a = [[0] * 2] * 2
    a[0][0] = 1
    print(a)""",
        "options": [
            "A. [[1, 0], [0, 0]]",
            "B. [[1, 0], [1, 0]]",
            "C. [[1, 1], [0, 0]]",
            "D. Lỗi TypeError",
        ],
        "answer": "B",
        "explain": "`[[0] * 2] * 2` tạo ra 2 tham chiếu trỏ tới CÙNG 1 list con. Sửa a[0][0] sẽ làm đổi cả a[1][0].",
    },
    {
        "q": """Câu 2: Kết quả của đoạn code sau là gì?
    def f(x, lst=[]):
        lst.append(x)
        return lst
    print(f(1), f(2))""",
        "options": [
            "A. [1] [2]",
            "B. [1] [1, 2]",
            "C. [1, 2] [1, 2]",
            "D. Lỗi UnboundLocalError",
        ],
        "answer": "C",
        "explain": "`f(1)` trả về tham chiếu tới `lst`, sau đó `f(2)` thêm `2` vào CHÍNH `lst` đó trước khi `print()` in cả 2 giá trị, nên cả 2 đều in `[1, 2]`!",
    },
    {
        "q": """Câu 3: Kết quả của đoạn code sau là gì?
    a = [1, 2, 3]
    b = [1, 2, 3]
    print(a == b, a is b)""",
        "options": [
            "A. True True",
            "B. True False",
            "C. False True",
            "D. False False",
        ],
        "answer": "B",
        "explain": "`==` so sánh giá trị (True), còn `is` so sánh địa chỉ bộ nhớ (2 list khác nhau -> False).",
    },
    {
        "q": """Câu 4: Kiểu dữ liệu của `x = (42)` là gì?""",
        "options": [
            "A. tuple",
            "B. int",
            "C. list",
            "D. Lỗi SyntaxError",
        ],
        "answer": "B",
        "explain": "Dấu ngoặc đơn không có dấu phẩy chỉ là biểu thức toán học -> `int`. Tuple 1 phần tử bắt buộc viết `(42,)`.",
    },
    {
        "q": """Câu 5: Kết quả của đoạn code sau là gì?
    funcs = [lambda: i for i in range(3)]
    print([fn() for fn in funcs])""",
        "options": [
            "A. [0, 1, 2]",
            "B. [2, 2, 2]",
            "C. [3, 3, 3]",
            "D. Lỗi NameError",
        ],
        "answer": "B",
        "explain": "Closure Late Binding: các lambda cùng tham chiếu tới biến `i` sau khi vòng lặp kết thúc (`i = 2`). Để ra `[0, 1, 2]`, phải viết `lambda i=i: i`.",
    },
    {
        "q": """Câu 6: Kết quả của đoạn code sau là gì?
    g = (x * 2 for x in range(3))
    print(list(g), list(g))""",
        "options": [
            "A. [0, 2, 4] [0, 2, 4]",
            "B. [0, 2, 4] []",
            "C. [] []",
            "D. Lỗi StopIteration",
        ],
        "answer": "B",
        "explain": "Generator là iterator chỉ duyệt được 1 lần. Sau `list(g)` đầu tiên, generator đã cạn nên lần thứ 2 trả về `[]`.",
    },
    {
        "q": """Câu 7: Kết quả của đoạn code sau là gì?
    nums = [1, 2, 3]
    print(nums[10:20])""",
        "options": [
            "A. Lỗi IndexError",
            "B. None",
            "C. []",
            "D. [3]",
        ],
        "answer": "C",
        "explain": "Indexing `nums[10]` báo `IndexError`, nhưng Slicing vượt biên `nums[10:20]` luôn an toàn và trả về `[]`.",
    },
    {
        "q": """Câu 8: Kết quả của đoạn code sau là gì?
    class A:
        x = 10
    a1, a2 = A(), A()
    a1.x = 20
    print(A.x, a1.x, a2.x)""",
        "options": [
            "A. 20 20 20",
            "B. 10 20 10",
            "C. 10 20 20",
            "D. 20 20 10",
        ],
        "answer": "B",
        "explain": "`a1.x = 20` tạo một instance attribute mới trên `a1`, không làm thay đổi class attribute `A.x` (nên `A.x` và `a2.x` vẫn là `10`).",
    },
    {
        "q": """Câu 9: Kết quả của hàm `test()` sau là gì?
    def test():
        try:
            return 1
        finally:
            return 2
    print(test())""",
        "options": [
            "A. 1",
            "B. 2",
            "C. 1 rồi 2",
            "D. Lỗi SyntaxError",
        ],
        "answer": "B",
        "explain": "Khối `finally` LUÔN chạy trước khi hàm thoát ra; nếu `finally` có `return`, giá trị của nó sẽ ghi đè `return` ở `try`.",
    },
    {
        "q": """Câu 10: Lệnh nào dùng để sắp xếp `d = {'a': 3, 'b': 1, 'c': 2}` theo giá trị (value) tăng dần?""",
        "options": [
            "A. sorted(d)",
            "B. d.sort(key=lambda x: x[1])",
            "C. sorted(d.items(), key=lambda item: item[1])",
            "D. sorted(d.values())",
        ],
        "answer": "C",
        "explain": "`sorted(d.items(), key=lambda item: item[1])` sắp xếp các cặp `(key, value)` theo `item[1]` (value) và giữ được cả key lẫn value.",
    },
    {
        "q": """Câu 11: Kết quả của đoạn code sau là gì?
    print(round(2.5), round(3.5))""",
        "options": ["A. 3 4", "B. 2 4", "C. 2 3", "D. 3 3"],
        "answer": "B",
        "explain": "`round()` dùng Banker's rounding: số đúng ở giữa (.5) được làm tròn về số CHẴN gần nhất -> round(2.5) = 2, round(3.5) = 4.",
    },
    {
        "q": """Câu 12: Kết quả của đoạn code sau là gì?
    x = [1, 2, 3]
    y = x
    x += [4]
    print(y)""",
        "options": ["A. [1, 2, 3]", "B. [1, 2, 3, 4]", "C. [4]", "D. Lỗi TypeError"],
        "answer": "B",
        "explain": "Với list, `x += [4]` sửa TẠI CHỖ (như `extend`) object mà cả x và y cùng trỏ tới. Nếu viết `x = x + [4]` thì y mới giữ nguyên [1, 2, 3].",
    },
    {
        "q": """Câu 13: Kết quả của đoạn code sau là gì?
    it = iter([1, 2, 3])
    next(it)
    print(list(it), list(it))""",
        "options": [
            "A. [1, 2, 3] [1, 2, 3]",
            "B. [2, 3] [2, 3]",
            "C. [2, 3] []",
            "D. [1, 2, 3] []",
        ],
        "answer": "C",
        "explain": "Iterator nhớ vị trí đang duyệt: `next(it)` đã lấy 1, `list(it)` lấy phần còn lại [2, 3] và làm iterator cạn, nên lần sau trả về [].",
    },
    {
        "q": """Câu 14: Kết quả của đoạn code sau là gì?
    print(sorted(["bb", "a", "dd", "ccc", "c"], key=len))""",
        "options": [
            "A. ['a', 'c', 'bb', 'dd', 'ccc']",
            "B. ['a', 'bb', 'c', 'ccc', 'dd']",
            "C. ['c', 'a', 'dd', 'bb', 'ccc']",
            "D. ['ccc', 'bb', 'dd', 'a', 'c']",
        ],
        "answer": "A",
        "explain": "Sắp theo độ dài tăng dần; `sorted` là sort ỔN ĐỊNH nên các phần tử cùng độ dài giữ nguyên thứ tự ban đầu ('a' trước 'c', 'bb' trước 'dd').",
    },
    {
        "q": """Câu 15: Kết quả khi gọi `outer()()` là gì?
    def outer():
        count = 0
        def inc():
            count += 1
            return count
        return inc""",
        "options": ["A. 1", "B. 0", "C. Lỗi UnboundLocalError", "D. Lỗi NameError"],
        "answer": "C",
        "explain": "`count += 1` là phép GÁN nên Python coi `count` là biến local của `inc`, nhưng đọc nó trước khi gán -> UnboundLocalError. Cần thêm `nonlocal count`.",
    },
    {
        "q": """Câu 16: Kết quả của đoạn code sau là gì?
    x = 5
    match 3:
        case x:
            print("khớp", x)""",
        "options": ["A. Không in gì", "B. khớp 5", "C. khớp 3", "D. Lỗi SyntaxError"],
        "answer": "C",
        "explain": "Trong `case`, một tên biến trần là CAPTURE pattern: luôn khớp và GÁN giá trị (3) vào x. Nó không so sánh với biến x = 5 bên ngoài.",
    },
    {
        "q": """Câu 17: Kết quả của đoạn code sau là gì?
    class A:
        @property
        def v(self):
            return 1
    a = A()
    a.v = 2
    print(a.v)""",
        "options": ["A. 2", "B. 1", "C. Lỗi AttributeError", "D. Lỗi TypeError"],
        "answer": "C",
        "explain": "`@property` không có `@v.setter` là thuộc tính CHỈ ĐỌC; gán `a.v = 2` báo AttributeError (property has no setter).",
    },
    {
        "q": """Câu 18: Kết quả của đoạn code sau là gì?
    try:
        int("x")
    except Exception:
        print("E")
    except ValueError:
        print("V")""",
        "options": ["A. V", "B. E", "C. E rồi V", "D. Lỗi chương trình"],
        "answer": "B",
        "explain": "Các `except` được xét từ trên xuống và chỉ chạy khối ĐẦU TIÊN khớp. ValueError là lớp con của Exception nên bị `except Exception` bắt trước. Luôn đặt exception cụ thể lên trước!",
    },
    {
        "q": r"""Câu 19: Kết quả của đoạn code sau là gì?
    import re
    print(re.match(r"\d+", "abc123"))""",
        "options": ["A. <re.Match object; ... match='123'>", "B. None", "C. '123'", "D. Lỗi re.error"],
        "answer": "B",
        "explain": "`re.match` chỉ thử khớp ở ĐẦU chuỗi ('a' không phải chữ số) -> None. Muốn tìm ở bất kỳ đâu phải dùng `re.search`.",
    },
    {
        "q": """Câu 20: Kết quả của đoạn code sau là gì?
    import random
    data = [3, 1, 2]
    print(random.shuffle(data))""",
        "options": ["A. [1, 2, 3]", "B. Một hoán vị ngẫu nhiên của [3, 1, 2]", "C. None", "D. Lỗi TypeError"],
        "answer": "C",
        "explain": "`random.shuffle` xáo trộn TẠI CHỖ và trả về None (giống `list.sort()`). Danh sách đã xáo nằm trong chính biến `data`.",
    },
]


# Câu hỏi số i (đếm từ 1) -> phần cần ôn lại nếu làm sai.
REVIEW = {
    1: "Module 01 §4 (bẫy ma trận 2D)",
    2: "Module 03 §1 (mutable default argument)",
    3: "Module 01 §2 (== và is)",
    4: "Module 02 §3 (tuple 1 phần tử)",
    5: "Module 03 §3 (closure late binding)",
    6: "Module 02 §7 (generator)",
    7: "Module 01 §6 (slicing)",
    8: "Module 04 §1 (class/instance attribute)",
    9: "Module 05 §4 (try/finally)",
    10: "Module 03 §3 (sorted với key)",
    11: "Module 01 §1 (round)",
    12: "Module 01 §4 (+= với list)",
    13: "Module 02 §9 (iterator)",
    14: "Module 02 §10 (sort ổn định)",
    15: "Module 03 §2 (closure & nonlocal)",
    16: "Module 01 §8 (match-case)",
    17: "Module 04 §2 (@property)",
    18: "Module 05 §4 (thứ tự except)",
    19: "Module 07 §1.4 (match/search)",
    20: "Module 07 §3.1 (random.shuffle)",
}


def run_quiz() -> None:
    score = 0
    wrong: list[int] = []
    total = len(QUESTIONS)
    print("=" * 60)
    print(f"BÀI TEST THỬ PYTHON ĐẦU VÀO ({total} CÂU HỎI)")
    print("Nhấn Ctrl+C để thoát giữa chừng.")
    print("=" * 60)

    for idx, item in enumerate(QUESTIONS, start=1):
        print(f"\n{item['q']}")
        for opt in item["options"]:
            print(f"  {opt}")

        while True:
            ans = input("Đáp án của bạn (A/B/C/D): ").strip().upper()
            if ans in {"A", "B", "C", "D"}:
                break
            print("Vui lòng chỉ nhập A, B, C hoặc D.")

        if ans == item["answer"]:
            print("-> CHÍNH XÁC!")
            score += 1
        else:
            print(f"-> SAI rồi! Đáp án đúng là {item['answer']}.")
            wrong.append(idx)
        print(f"   Giải thích: {item['explain']}")

    print("\n" + "=" * 60)
    print(f"KẾT QUẢ: {score}/{total} câu đúng ({score / total:.0%})")
    if score >= 0.8 * total:
        print("Xuất sắc! Bạn đã sẵn sàng cho bài test Python đầu vào & học AI.")
    else:
        print("Chưa đạt mức 80%. Hãy ôn lại các phần dưới đây rồi làm lại nhé!")
    if wrong:
        print("\nCác phần cần ôn lại:")
        for idx in wrong:
            print(f"  - Câu {idx}: {REVIEW.get(idx, '')}")


if __name__ == "__main__":
    try:
        run_quiz()
    except (KeyboardInterrupt, EOFError):
        print("\nĐã thoát bài test.")

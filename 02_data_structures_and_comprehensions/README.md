# Module 02: Cấu trúc dữ liệu, Comprehensions & Generators (Chi tiết)

Nắm chắc 4 cấu trúc dữ liệu tích hợp (`list`, `tuple`, `dict`, `set`) cùng `comprehensions` và `generators` là bạn đã làm chủ được **phần lớn câu hỏi thuật toán & xử lý dữ liệu** trong bài test Python cũng như tiền xử lý dữ liệu AI.

---

## 1. Tổng quan & Độ phức tạp (Big-O)

| Kiểu | Thứ tự | Thay đổi được? | Trùng lặp? | Tìm kiếm `x in c` | Khi nào dùng? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `list` | Có | Mutable | Có | $O(n)$ | Danh sách mẫu dữ liệu, batches, chuỗi có thứ tự |
| `tuple` | Có | Immutable | Có | $O(n)$ | Shape tensor `(32, 3, 224, 224)`, tọa độ, làm key của `dict` |
| `dict` | Có (từ 3.7+) | Mutable | Key không trùng | $O(1)$ | Từ điển `token -> id`, đếm tần suất, config |
| `set` | Không | Mutable | Không | $O(1)$ | Lọc từ trùng lặp, kiểm tra tồn tại siêu nhanh (stopwords) |

---

## 2. `list`: Các method & Bẫy hay gặp

```python
nums = [3, 1, 4]

# Thêm phần tử: append vs extend (HAY RA TRONG TEST!)
nums.append([5, 6])   # [3, 1, 4, [5, 6]]  -> thêm cả list làm 1 phần tử
nums = [3, 1, 4]
nums.extend([5, 6])   # [3, 1, 4, 5, 6]    -> nối từng phần tử vào cuối

# Xóa phần tử
last = nums.pop()     # Lấy và xóa phần tử cuối (pop(0) chậm O(n)!)
nums.remove(1)        # Xóa giá trị 1 đầu tiên tìm thấy (báo ValueError nếu không có)

# Sắp xếp: .sort() vs sorted() (HAY BỊ NHẦM!)
a = [3, 1, 2]
res = a.sort()        # res là None! .sort() sửa trực tiếp trên `a` (in-place)
b = sorted(a, reverse=True)  # Trả về list MỚI [3, 2, 1], không sửa `a`
```

> **Bẫy xóa phần tử khi đang duyệt `for`:**
> Không bao giờ `remove()` trực tiếp trên list đang lặp (sẽ bị nhảy cóc phần tử). Hãy tạo list mới bằng list comprehension: `nums = [x for x in nums if x > 0]`.

---

## 3. `tuple`: Bất biến & Unpacking

```python
# Bẫy Tuple 1 phần tử (Cực hay hỏi!):
not_a_tuple = (42)    # Đây là int!
is_a_tuple  = (42,)   # Phải có dấu phẩy!

# Unpacking & Swap
a, b = 10, 20
a, b = b, a           # Hoán đổi giá trị không cần biến tạm!

shape = (32, 3, 224, 224)
batch, *spatial = shape   # batch = 32, spatial = [3, 224, 224]
```

---

## 4. `dict`: Key-Value tốc độ $O(1)$

- **Key của `dict` phải là kiểu Hashable (bất biến)**: `int`, `str`, `tuple` (chứa phần tử bất biến) làm key được; `list` và `dict` **không** làm key được (`TypeError: unhashable type`).

```python
vocab = {"ai": 1, "python": 2}

# Truy cập an toàn:
# vocab["java"]           -> KeyError!
vocab.get("java", 0)      # Trả về 0 nếu không có key (không báo lỗi)

# Duyệt dict
for key in vocab:                  # Duyệt keys
    pass
for k, v in vocab.items():         # Duyệt cả key và value
    print(k, v)

# Gộp 2 dict (Python 3.9+)
default_cfg = {"lr": 1e-3, "epochs": 10}
user_cfg = {"epochs": 20, "device": "cuda"}
final_cfg = default_cfg | user_cfg  # {'lr': 1e-3, 'epochs': 20, 'device': 'cuda'}
```

---

## 5. `set`: Tập hợp không trùng lặp

```python
# Bẫy khởi tạo set rỗng:
empty_dict = {}       # Đây là dict!
empty_set = set()     # Đây mới là set rỗng!

a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

a | b   # Hợp (Union): {1, 2, 3, 4, 5, 6}
a & b   # Giao (Intersection): {3, 4}
a - b   # Hiệu (Difference): {1, 2}
a ^ b   # Đối xứng (Có ở a hoặc b nhưng không cả hai): {1, 2, 5, 6}
```

> **Mẹo phỏng vấn:** Kiểm tra `x in my_set` mất $O(1)$, còn `x in my_list` mất $O(n)$. Nếu cần lọc 100,000 từ theo danh sách stopwords, luôn chuyển stopwords thành `set` trước!

---

## 6. `enumerate()` & `zip()`

```python
tokens = ["I", "love", "AI"]
for idx, tok in enumerate(tokens, start=1):
    print(idx, tok)   # 1 I, 2 love, 3 AI

# zip() ghép nhiều list song song, tự dừng ở list NGẮN NHẤT
names = ["loss", "acc", "f1"]
vals = [0.25, 0.91]
dict(zip(names, vals))   # {'loss': 0.25, 'acc': 0.91}

# Mẹo cực hay: Chuyển vị ma trận (Transpose) bằng zip(*matrix)
matrix = [[1, 2, 3], [4, 5, 6]]
list(zip(*matrix))       # [(1, 4), (2, 5), (3, 6)]
```

---

## 7. Comprehensions & Generators (`yield`)

### Comprehensions
```python
# List comprehension + điều kiện lọc
evens = [x for x in range(10) if x % 2 == 0]

# List comprehension với if-else (lưu ý vị trí if-else đứng TRƯỚC for!)
labels = ["pos" if s >= 0.5 else "neg" for s in [0.8, 0.2, 0.6]]

# Dict & Set comprehension
id_to_tok = {v: k for k, v in vocab.items()}
unique_lens = {len(t) for t in tokens}
```

### Generator & `yield` (Cực quan trọng cho dữ liệu lớn)
- List comprehension `[x*2 for x in range(10**7)]` nhồi **toàn bộ 10 triệu số vào RAM** ngay lập tức.
- Generator `(x*2 for x in range(10**7))` hoặc hàm dùng `yield` chỉ sinh ra từng phần tử khi được hỏi (**Lazy Evaluation**), tốn gần như **0 RAM**.

```python
gen = (x * 2 for x in range(3))
print(list(gen))  # [0, 2, 4]
print(list(gen))  # [] -> BẪY: Generator/Iterator chỉ duyệt được MỘT LẦN rồi cạn!
```

---

## 8. Module `collections` (`Counter`, `defaultdict`, `deque`)

```python
from collections import Counter, defaultdict, deque

# Counter: đếm tần suất cực nhanh
counts = Counter(["cat", "dog", "cat", "bird", "cat"])
counts.most_common(2)    # [('cat', 3), ('dog', 2)]

# defaultdict: tự khởi tạo giá trị mặc định khi key chưa tồn tại
groups = defaultdict(list)
groups["train"].append("img1.png")  # Không cần kiểm tra `if "train" not in groups`

# deque: hàng đợi 2 đầu, thêm/xóa ở ĐẦU (popleft/appendleft) chỉ mất O(1) thay vì O(n) như list
buffer = deque(maxlen=3)  # Tự động đẩy phần tử cũ nhất ra khi đầy (làm Replay Buffer trong RL!)
```

---

## 9. Iterable, Iterator & cơ chế thật sự của vòng `for`

Hai khái niệm hay bị nhầm (và hay bị hỏi):

| | **Iterable** | **Iterator** |
| :--- | :--- | :--- |
| Định nghĩa | Thứ **có thể duyệt được**: có `__iter__()` | Thứ **đang duyệt**: có `__next__()` (và `__iter__()` trả về chính nó) |
| Ví dụ | `list`, `tuple`, `str`, `dict`, `set`, `range`, file | Generator, `iter(list)`, `zip(...)`, `map(...)`, `enumerate(...)` |
| Duyệt nhiều lần? | **Có**: mỗi lần `for` tạo một iterator mới | **Không**: duyệt hết là cạn |

Vòng `for x in data:` thực chất là:

```python
it = iter(data)          # 1. gọi data.__iter__() để lấy iterator
while True:
    try:
        x = next(it)     # 2. gọi it.__next__() để lấy phần tử kế tiếp
    except StopIteration:
        break            # 3. hết phần tử thì iterator raise StopIteration và vòng lặp dừng
    ...                  # thân vòng for
```

Thử trong REPL:

```python
it = iter([10, 20, 30])
next(it)          # 10
next(it)          # 20
list(it)          # [30]  -> chỉ còn phần chưa duyệt!
next(it)          # StopIteration
next(it, None)    # None  -> tham số thứ 2 là giá trị mặc định, tránh lỗi

z = zip([1, 2], ["a", "b"])
list(z)           # [(1, 'a'), (2, 'b')]
list(z)           # []  -> zip, map, filter, enumerate đều là iterator: chỉ dùng được 1 lần!
```

> **Góc nhìn AI:** `DataLoader` của PyTorch là **iterable** (mỗi epoch `for batch in loader:` tạo iterator mới và shuffle lại), còn `iter(loader)` là **iterator**. Câu `batch = next(iter(loader))` để lấy thử 1 batch xuất hiện trong hầu hết các notebook. Bạn sẽ tự viết một class iterable ở Module 04.

---

## 10. Sắp xếp nâng cao, `min`/`max` với `key`, `heapq` & `itertools`

### `key=` dùng được với `sorted`, `min`, `max`
```python
words = ["banana", "kiwi", "apple", "fig", "cherry", "date"]

sorted(words, key=len)                   # ['fig', 'kiwi', 'date', 'apple', 'banana', 'cherry']
sorted(words, key=lambda w: (len(w), w)) # Sắp theo NHIỀU tiêu chí bằng tuple (độ dài, rồi a→z):
                                         # ['fig', 'date', 'kiwi', 'apple', 'banana', 'cherry']
sorted(words, key=lambda w: (-len(w), w))# Dài trước; cùng độ dài thì a→z:
                                         # ['banana', 'cherry', 'apple', 'date', 'kiwi', 'fig']
max(words, key=len)                      # 'banana' (phần tử ĐẦU TIÊN có len lớn nhất)

scores = {"doc1": 0.42, "doc2": 0.91, "doc3": 0.75}
max(scores, key=scores.get)              # 'doc2' -> key có value lớn nhất (argmax!)
```

> **Sort ổn định (stable):** Khi 2 phần tử có key bằng nhau, `sorted()` **giữ nguyên thứ tự ban đầu** của chúng. Với `key=len`, `"kiwi"` đứng trước `"date"` (cùng dài 4) chỉ vì trong list gốc nó đứng trước, chứ không phải do thứ tự a→z. Muốn cùng độ dài thì xếp a→z, phải dùng key tuple như dòng thứ hai.

### `heapq`: lấy Top-K mà không cần sort toàn bộ
```python
import heapq

nums = [5, 1, 8, 3, 9, 2]
heapq.nlargest(3, nums)                  # [9, 8, 5]
heapq.nsmallest(2, nums)                 # [1, 2]
heapq.nlargest(2, scores.items(), key=lambda kv: kv[1])   # [('doc2', 0.91), ('doc3', 0.75)]
```
- `sorted(...)[:k]` tốn $O(n \log n)$; `heapq.nlargest(k, ...)` tốn $O(n \log k)$, nhanh hơn rõ rệt khi $n$ lớn và $k$ nhỏ.
- **Góc nhìn AI:** Đây chính là bước lấy **Top-K tài liệu** trong RAG hoặc **Top-K token** khi sampling của LLM.

### `itertools`: công cụ cho iterator
```python
from itertools import islice, chain, count, cycle, product, accumulate

list(islice(range(100), 3))              # [0, 1, 2]  -> "slicing" cho iterator/generator
list(chain([1, 2], [3], [4, 5]))         # [1, 2, 3, 4, 5] -> nối nhiều iterable
list(islice(count(10), 3))               # [10, 11, 12] -> đếm vô hạn (phải dùng kèm islice!)
list(islice(cycle("AB"), 5))             # ['A', 'B', 'A', 'B', 'A'] -> lặp vô hạn
list(product([0.1, 0.01], [16, 32]))     # [(0.1, 16), (0.1, 32), (0.01, 16), (0.01, 32)]
list(accumulate([1, 2, 3, 4]))           # [1, 3, 6, 10] -> tổng tích lũy
```

> **Góc nhìn AI:** `product(...)` dùng để tạo lưới hyperparameter (grid search); `islice(stream, n)` dùng để lấy thử `n` mẫu từ một dataset streaming khổng lồ mà không cần tải hết.

---

## Thực hành

Mở [exercises.py](./exercises.py) và chạy kiểm tra:
```bash
python3 02_data_structures_and_comprehensions/exercises.py
```

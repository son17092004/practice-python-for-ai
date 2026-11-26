# Module 03: Functions, Scope, Type Hints & Decorators (Chi tiết)

Phần này giải thích đầy đủ cơ chế hàm trong Python — từ các tham số linh hoạt, quy tắc phạm vi biến (LEGB) cho tới những câu bẫy kinh điển như **Mutable Default Argument** hay **Closure Late Binding**.

---

## 1. Tham số hàm & Thứ tự truyền

```python
# Thứ tự chuẩn: (positional, *args, keyword-only, **kwargs)
def train_step(data, lr=1e-3, *args, device="cpu", **kwargs):
    print(f"lr={lr}, args={args}, device={device}, kwargs={kwargs}")

# Lưu ý: tham số đứng SAU `*` hoặc `*args` là keyword-only (bắt buộc gọi tên)
train_step([1, 2], 0.01, "extra", device="cuda", epochs=10)
```

### Bẫy kinh điển #1: Mutable Default Argument
Giá trị mặc định của hàm chỉ được khởi tạo **MỘT LẦN DUY NHẤT** lúc `def` được thực thi, KHÔNG phải mỗi lần gọi hàm!

```python
# SAI:
def add_item(x, items=[]):
    items.append(x)
    return items

add_item(1)  # [1]
add_item(2)  # [1, 2] -> Bị dính dữ liệu từ lần gọi trước!

# ĐÚNG: Dùng None
def add_item_safe(x, items: list | None = None) -> list:
    if items is None:
        items = []
    items.append(x)
    return items
```

### Unpacking khi gọi hàm (`*` và `**`)
```python
def create_model(name: str, lr: float, epochs: int):
    return f"{name} (lr={lr}, epochs={epochs})"

cfg = {"lr": 3e-4, "epochs": 10}
create_model("Transformer", **cfg)  # Tương đương create_model("Transformer", lr=3e-4, epochs=10)
```
> **Góc nhìn AI:** Trong PyTorch và HuggingFace, bạn sẽ gặp `def forward(self, *args, **kwargs)` và `AutoModel.from_pretrained(model_id, **config)` ở khắp mọi nơi.

---

## 2. Phạm vi biến: Quy tắc LEGB

Python tìm tên biến theo đúng thứ tự 4 tầng:
1. **L (Local)**: Bên trong hàm hiện tại.
2. **E (Enclosing)**: Bên trong hàm cha bao bọc (nếu là hàm lồng nhau).
3. **G (Global)**: Cấp độ module/file.
4. **B (Built-in)**: Các tên có sẵn của Python (`len`, `sum`, `max`...).

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        nonlocal x   # Nếu muốn SỬA biến của `outer`, dùng `nonlocal` (sửa global dùng `global`)
        x = "modified"
    inner()
    print(x)         # "modified"
```

> **Bẫy hay gặp:** Nếu trong hàm bạn gán `x = 5` ở cuối hàm nhưng lại `print(x)` ở đầu hàm (dù bên ngoài có biến global `x`), Python sẽ báo `UnboundLocalError` vì nó coi `x` là biến Local của cả hàm!

### Closure: hàm "nhớ" biến của hàm cha

Một hàm con được trả về từ hàm cha vẫn **giữ được** các biến của hàm cha, kể cả khi hàm cha đã chạy xong. Đây gọi là **closure**:

```python
def make_counter():
    count = 0
    def inc():
        nonlocal count     # thiếu dòng này -> UnboundLocalError (vì `count += 1` là phép GÁN)
        count += 1
        return count
    return inc

c1 = make_counter()
c2 = make_counter()        # mỗi lần gọi make_counter() tạo một `count` riêng
c1(), c1(), c2()           # (1, 2, 1)
```

- **Đọc** biến của hàm cha thì không cần `nonlocal`.
- **Gán lại** (`=`, `+=`) thì bắt buộc phải có `nonlocal`.
- **Mutate** một list/dict của hàm cha (`.append`, `d[k] = v`) thì không cần `nonlocal`, vì đó không phải phép gán tên.

> **Góc nhìn AI:** Closure là nền tảng của decorator (mục 5), và của các hàm "factory" như `make_lr_scheduler(base_lr)`, vốn trả về một hàm tính learning rate theo từng bước.

---

## 3. Lambda, `sorted(..., key=...)`, `any()`, `all()`

Hàm trong Python là **First-class object** (có thể gán vào biến, truyền vào hàm khác, trả về từ hàm).

```python
# sorted() với key: cực kỳ hay dùng để xếp hạng kết quả AI (RAG, Top-K predictions)
results = [("doc1", 0.42), ("doc2", 0.91), ("doc3", 0.75)]
ranked = sorted(results, key=lambda item: item[1], reverse=True)
# -> [('doc2', 0.91), ('doc3', 0.75), ('doc1', 0.42)]

# any() và all(): trả về bool (hỗ trợ short-circuit, rất gọn)
scores = [0.8, 0.9, 0.4]
all(s >= 0.5 for s in scores)   # False (tất cả >= 0.5?)
any(s >= 0.85 for s in scores)  # True (có ít nhất 1 cái >= 0.85?)
```

### Bẫy kinh điển #2: Closure Late Binding trong vòng lặp
```python
# SAI: Tất cả hàm lambda đều trỏ tới giá trị CUỐI CÙNG của `i` (là 2)!
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])  # [2, 2, 2] -> Không phải [0, 1, 2]!

# ĐÚNG: Bắt giá trị `i` tại mỗi vòng bằng default argument
funcs_ok = [lambda i=i: i for i in range(3)]
print([f() for f in funcs_ok])  # [0, 1, 2]
```

---

## 4. Type Hints (Python 3.10+)

Type Hints giúp code rõ ràng như tài liệu sống, IDE gợi ý chính xác và dễ debug shape/kiểu dữ liệu (lưu ý Python không tự kiểm tra kiểu lúc chạy nếu không dùng công cụ như `mypy`).

```python
from typing import Callable, Any

def preprocess(
    texts: list[str],
    transform: Callable[[str], str],
    max_len: int | None = None,
) -> list[str]:
    out = [transform(t) for t in texts]
    return [t[:max_len] for t in out] if max_len is not None else out
```

---

## 5. Decorators & `@functools.wraps` / `@cache`

Decorator là một hàm nhận vào một hàm khác và trả về hàm mới đã được mở rộng chức năng.

```python
import time
from functools import wraps, lru_cache

def timer(func):
    @wraps(func)  # Giữ nguyên __name__ và docstring của `func` gốc!
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} chạy mất {time.perf_counter() - t0:.4f}s")
        return result
    return wrapper

@timer
def slow_fn():
    return sum(range(1_000_000))

# Decorator tích hợp cực hữu ích: Memoization (cache kết quả hàm đệ quy / tính toán lặp)
@lru_cache(maxsize=128)
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

> **Góc nhìn AI:** Trong PyTorch, `@torch.no_grad()` là một decorator/context-manager tắt việc tính gradient khi inference để tiết kiệm RAM GPU và tăng tốc độ.

---

## 6. Đệ quy (Recursion)

Hàm đệ quy là hàm **tự gọi lại chính nó** với một bài toán nhỏ hơn. Mọi hàm đệ quy cần đủ 2 phần:
1. **Base case (điểm dừng)**: trường hợp đủ đơn giản để trả kết quả ngay.
2. **Recursive case**: thu nhỏ bài toán rồi gọi lại chính hàm đó.

```python
def factorial(n: int) -> int:
    if n <= 1:                 # 1. base case
        return 1
    return n * factorial(n - 1)  # 2. recursive case: bài toán nhỏ hơn

# Đệ quy tỏa sáng với dữ liệu LỒNG NHAU không biết trước độ sâu:
def count_leaves(tree) -> int:
    if not isinstance(tree, list):     # lá
        return 1
    return sum(count_leaves(child) for child in tree)

count_leaves([1, [2, 3], [[4], 5]])    # 5
```

**Các bẫy cần nhớ:**
- **Quên base case**, hoặc base case không bao giờ chạm tới, sẽ gây `RecursionError: maximum recursion depth exceeded`. Giới hạn mặc định khoảng 1000 tầng (`sys.getrecursionlimit()`).
- **Tính lặp lại**: `fib(n)` đệ quy thuần tốn $O(2^n)$. Thêm `@lru_cache` / `@cache` (mục 5) sẽ giảm xuống còn $O(n)$.
- Python **không** tối ưu đệ quy đuôi (tail-call). Với dữ liệu rất sâu (hàng chục nghìn tầng), hãy viết lại bằng vòng lặp kết hợp một list làm stack.

> **Góc nhìn AI:** Đệ quy xuất hiện khi duyệt cấu trúc lồng nhau: config YAML/JSON nhiều tầng, cây thư mục dataset, cây quyết định (Decision Tree), hoặc hàm `tree_map` để áp dụng một phép biến đổi lên mọi tensor trong một dict/list lồng nhau.

---

## Thực hành

Mở [exercises.py](./exercises.py) và chạy kiểm tra:
```bash
python3 03_functions_typing_and_decorators/exercises.py
```

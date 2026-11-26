# Module 01: Core Syntax, Mutability, Strings & Slicing (Chi tiết)

Module này giúp bạn nắm lại **80–90% kiến thức cốt lõi của Python** — những thứ chắc chắn xuất hiện trong mọi bài test Python đầu vào cũng như trong code AI hằng ngày.

---

## 1. Biến, Kiểu dữ liệu & Ép kiểu

Python là ngôn ngữ **Dynamic Typing** (biến không gắn cố định kiểu, giá trị mới có kiểu), nhưng **Strongly Typed** (không tự động cộng `int` với `str` như JavaScript).

```python
x = 10          # int
y = 3.14        # float
name = "AI"     # str
flag = True     # bool (lưu ý: bool là lớp con của int! True == 1, False == 0)
empty = None    # NoneType

# Kiểm tra kiểu: ưu tiên isinstance() hơn type() vì hỗ trợ kế thừa
type(x)               # <class 'int'>
isinstance(x, int)    # True
isinstance(True, int) # True (bẫy hay gặp!)

# Ép kiểu
int("42")       # 42
int(3.99)       # 3 (cắt phần thập phân, KHÔNG làm tròn!)
float("3.5")    # 3.5
str(100)        # "100"
```

> **Lưu ý số thực (Floating-point precision):** `0.1 + 0.2 == 0.3` trả về `False` (`0.30000000000000004`). Khi test hoặc so sánh loss/accuracy trong AI, luôn dùng `math.isclose(a, b)` hoặc `abs(a - b) < 1e-9`.

### Bẫy `round()`: làm tròn kiểu "ngân hàng" (Banker's rounding)

`round()` của Python **không** làm tròn ".5 lên" như ở trường. Khi đúng ở giữa, nó làm tròn về **số chẵn gần nhất**:

```python
round(2.5)       # 2  (không phải 3!)
round(3.5)       # 4
round(-2.5)      # -2
round(2.675, 2)  # 2.67 (không phải 2.68!) vì 2.675 thực ra được lưu là 2.67499999...

# So sánh 4 cách "bỏ phần thập phân":
import math
int(-2.7)         # -2  (cắt bỏ, tiến về 0)
math.floor(-2.7)  # -3  (làm tròn xuống)
math.ceil(-2.2)   # -2  (làm tròn lên)
round(-2.7)       # -3  (gần nhất)
```

> **Góc nhìn AI:** Khi hiển thị metric, hãy dùng f-string `f"{acc:.2f}"` thay vì `round()`. Khi cần làm tròn ".5 lên" chính xác (tiền tệ, chấm điểm), dùng `decimal.Decimal` với `ROUND_HALF_UP`.

---

## 2. Toán tử & Các bẫy hay gặp trong Test đầu vào

### Toán tử số học
- `/` : Chia thực, **luôn trả về `float`** (`4 / 2 == 2.0`).
- `//`: Chia lấy phần nguyên làm tròn xuống (floor division): `7 // 2 == 3`, nhưng `-7 // 2 == -4` (làm tròn về âm vô cực, rất hay bị hỏi!).
- `%` : Chia lấy dư: `7 % 2 == 1`.
- `**`: Lũy thừa: `2 ** 3 == 8`.

### `==` vs `is` (Cực kỳ hay ra trong bài test!)
- `==`: So sánh **giá trị** (hai object có bằng nhau về nội dung không).
- `is`: So sánh **danh tính / địa chỉ bộ nhớ** (`id(a) == id(b)` — có phải cùng một object không).

```python
a = [1, 2, 3]
b = [1, 2, 3]
a == b   # True (cùng giá trị)
a is b   # False (hai list khác nhau trong bộ nhớ)

# Luôn dùng `is` hoặc `is not` khi kiểm tra None:
x = None
if x is None:
    print("Rỗng")
```

### So sánh chuỗi (Chained Comparison) & Short-circuit
```python
score = 85
if 0 <= score <= 100:   # Hợp lệ trong Python! Tương đương (0 <= score) and (score <= 100)
    print("Hợp lệ")

# `or` và `and` trả về GIÁ TRỊ của toán hạng quyết định kết quả, không chỉ True/False:
name = "" or "Anonymous"     # "Anonymous"
val = 0 and 100              # 0 (dừng ngay ở 0, không đánh giá vế sau)
```

---

## 3. Truthiness & Falsy Values

Trong câu lệnh `if`, Python tự động đánh giá mọi object thành `True` hoặc `False`.
Chỉ có **8 nhóm giá trị Falsy** (còn lại đều là Truthy):
1. `False`
2. `None`
3. `0`, `0.0`, `0j`
4. `""` (chuỗi rỗng)
5. `[]` (list rỗng)
6. `()` (tuple rỗng)
7. `{}` (dict rỗng)
8. `set()`, `range(0)`

```python
items = []
if not items:   # Chuẩn Pythonic (thay vì viết `if len(items) == 0:`)
    print("Danh sách rỗng")
```

---

## 4. Mutability (Khả biến) & Bẫy Copy dữ liệu

| Nhóm | Kiểu dữ liệu | Đặc điểm |
| :--- | :--- | :--- |
| **Immutable (Bất biến)** | `int`, `float`, `bool`, `str`, `tuple`, `frozenset`, `None` | Không thể sửa nội dung tại chỗ. Mọi phép biến đổi đều tạo object mới. |
| **Mutable (Khả biến)** | `list`, `dict`, `set` | Có thể thêm/sửa/xóa trực tiếp tại cùng địa chỉ bộ nhớ. |

### Shallow Copy vs Deep Copy
```python
import copy

# 1. Gán trực tiếp: chung vùng nhớ
a = [[1, 2], [3, 4]]
b = a
b[0][0] = 99   # a[0][0] cũng thành 99!

# 2. Shallow copy (a.copy(), a[:], list(a)): chỉ copy lớp ngoài!
c = a.copy()
c.append([5, 6])  # a KHÔNG bị thêm [5, 6]
c[0][0] = 777     # NHƯNG list con bên trong vẫn dùng chung -> a[0][0] thành 777!

# 3. Deep copy: copy độc lập hoàn toàn mọi lớp lồng nhau
d = copy.deepcopy(a)
d[0][0] = 0       # a hoàn toàn an toàn!
```

### Bẫy `+=` với list (Hay ra trong test!)
Với list, `x += [4]` **sửa tại chỗ** (giống `x.extend([4])`), còn `x = x + [4]` **tạo list mới**:

```python
x = [1, 2, 3]
y = x
x += [4]        # sửa chính object mà cả x và y cùng trỏ tới
print(y)        # [1, 2, 3, 4]  -> y bị đổi theo!

x = [1, 2, 3]
y = x
x = x + [4]     # x trỏ sang list MỚI, y vẫn giữ list cũ
print(y)        # [1, 2, 3]

# Với kiểu immutable (int, str, tuple), += luôn tạo object mới:
s = "ab"; t = s; s += "c"
print(t)        # "ab"
```

### Bẫy tạo ma trận 2D (Kinh điển trong Test Python & AI)
```python
# SAI: Cả 3 hàng trỏ tới CÙNG 1 list!
bad_grid = [[0] * 3] * 3
bad_grid[0][0] = 1
print(bad_grid)  # [[1, 0, 0], [1, 0, 0], [1, 0, 0]] -> Toang!

# ĐÚNG: Dùng list comprehension để tạo 3 list độc lập
good_grid = [[0] * 3 for _ in range(3)]
good_grid[0][0] = 1
print(good_grid) # [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
```

> **Góc nhìn AI:** Khi chuẩn hóa dữ liệu (normalize) hoặc augment ảnh/text, nếu không copy đúng cách, bạn sẽ vô tình làm hỏng tập dữ liệu gốc hoặc làm rò rỉ dữ liệu giữa train và validation.

---

## 5. String (`str`) & F-strings

Chuỗi trong Python là **immutable** (không thể làm `s[0] = "A"`).

### Các method bắt buộc phải nhớ (dùng suốt trong làm sạch dữ liệu NLP & Test)
```python
s = "  Hello, Python AI!  "

s.strip()                # "Hello, Python AI!" (xóa khoảng trắng 2 đầu; có lstrip/rstrip)
s.lower()                # "  hello, python ai!  " (chuyển thường; có upper, title)
s.strip().split(", ")    # ["Hello", "Python AI!"] (tách chuỗi thành list)
"-".join(["a", "b", "c"])# "a-b-c" (nối list chuỗi — nhanh hơn cộng chuỗi += rất nhiều!)
s.replace("AI", "ML")    # Thay thế chuỗi con
s.find("Python")         # Trả về index đầu tiên (hoặc -1 nếu không thấy; khác index() ở chỗ không raise lỗi)
"AI" in s                # True (kiểm tra chuỗi con)
s.strip().startswith("Hello")  # True (có endswith)
"12345".isdigit()        # True (kiểm tra toàn số)
```

### F-strings (Định dạng chuỗi hiện đại)
```python
epoch, loss, acc = 3, 0.04567, 0.925
print(f"Epoch {epoch:02d} | Loss: {loss:.4f} | Acc: {acc:.2%}")
# -> Epoch 03 | Loss: 0.0457 | Acc: 92.50%

# Debug nhanh biến và giá trị:
lr = 3e-4
print(f"{lr=}")          # -> lr=0.0003
```

---

## 6. Slicing (`[start:stop:step]`)

Quy tắc vàng: **Lấy từ `start` đến trước `stop`** (nửa khoảng `[start, stop)`).

```python
arr = [10, 20, 30, 40, 50, 60]

arr[0]       # 10 (index dương đếm từ 0)
arr[-1]      # 60 (index âm đếm từ cuối: -1 là phần tử cuối)
arr[1:4]     # [20, 30, 40]
arr[:3]      # [10, 20, 30] (mặc định start = 0)
arr[3:]      # [40, 50, 60] (mặc định stop = len(arr))
arr[-2:]     # [50, 60] (2 phần tử cuối)
arr[::2]     # [10, 30, 50] (bước nhảy 2)
arr[::-1]    # [60, 50, 40, 30, 20, 10] (đảo ngược list/str)

# Điểm khác biệt hay hỏi:
# arr[100]      -> IndexError!
# arr[100:200]  -> [] (Slicing vượt biên KHÔNG bao giờ báo lỗi!)
```

> **Góc nhìn AI:** Cú pháp slicing này giống hệt khi bạn cắt chiều dữ liệu trong NumPy/PyTorch (ví dụ: `X_train, X_test = X[:800], X[800:]` hoặc lấy token cuối `logits[:, -1, :]`).

---

## 7. Control Flow (`if`, `for`, `while`, `for...else`)

```python
# 1. Toán tử 3 ngôi (Ternary)
device = "cuda" if has_gpu else "cpu"

# 2. range(start, stop, step)
list(range(5))         # [0, 1, 2, 3, 4]
list(range(2, 10, 3))  # [2, 5, 8]
list(range(5, 0, -1))  # [5, 4, 3, 2, 1]

# 3. `for ... else` (Hay ra trong đề test Python!)
# Khối `else` CHỈ chạy nếu vòng lặp kết thúc tự nhiên (KHÔNG bị `break`).
nums = [2, 4, 6]
for n in nums:
    if n % 2 != 0:
        print("Tìm thấy số lẻ!")
        break
else:
    print("Tất cả đều là số chẵn!")  # Dòng này sẽ chạy
```

### `while`, `break`, `continue`

- `while điều_kiện:` lặp **khi chưa biết trước số vòng** (ví dụ: train đến khi loss đủ nhỏ, đọc đến khi hết dữ liệu).
- `break`: **thoát hẳn** vòng lặp gần nhất.
- `continue`: **bỏ qua phần còn lại** của vòng hiện tại, nhảy sang vòng kế tiếp.
- `while` cũng có `else`, với cùng quy tắc: chỉ chạy khi vòng lặp **không** bị `break`.

```python
# Ví dụ: giảm learning rate đến khi nhỏ hơn ngưỡng
lr, steps = 1.0, 0
while lr >= 0.01:
    lr *= 0.5
    steps += 1
print(steps, lr)     # 7 0.0078125

# continue: bỏ qua mẫu lỗi, break: dừng khi gặp dấu hiệu kết thúc
for line in ["a", "", "b", "<END>", "c"]:
    if not line:
        continue      # bỏ dòng trống, sang vòng tiếp
    if line == "<END>":
        break         # dừng hẳn, "c" không bao giờ được xử lý
    print(line)       # in ra: a, b

# Vòng lặp vô hạn có điểm thoát: mẫu rất hay gặp
while True:
    cmd = input("> ")
    if cmd == "quit":
        break
```

> **Bẫy:** `break` và `continue` chỉ tác động lên vòng lặp **gần nhất** (vòng trong cùng). Muốn thoát cả 2 vòng lồng nhau, hãy tách vòng lặp ra thành hàm rồi dùng `return`.

### Walrus operator `:=` (Python 3.8+)

Toán tử `:=` vừa **gán** vừa **trả về giá trị** ngay trong biểu thức, giúp tránh tính một thứ hai lần:

```python
# Không có walrus: phải gọi len() 2 lần hoặc tách thêm dòng
data = list(range(15))
if (n := len(data)) > 10:
    print(f"Dữ liệu quá dài ({n} phần tử)")

# Đọc file theo từng khối đến khi hết
# while (chunk := f.read(1024)):
#     process(chunk)

# Trong comprehension: tính một lần, vừa lọc vừa dùng
scores = [s for x in [1, 2, 3, 4] if (s := x * x) > 4]   # [9, 16]
```

---

## 8. `match-case`: Structural Pattern Matching (Python 3.10+)

`match` **không chỉ** là `switch` của C/Java: nó so khớp được cả **cấu trúc** (list, tuple, dict, class) và **bóc tách** giá trị ra biến.

```python
def handle(command: str) -> str:
    match command.split():
        case ["train", epochs] if epochs.isdigit():   # khớp list 2 phần tử + điều kiện (guard)
            return f"Train {epochs} epochs"
        case ["eval"]:                                 # khớp đúng list ["eval"]
            return "Evaluate"
        case ["save", *paths]:                         # *paths gom phần còn lại
            return f"Save to {paths}"
        case ["quit" | "exit"]:                        # | nghĩa là "hoặc"
            return "Bye"
        case _:                                        # _ = mặc định (khớp mọi thứ)
            return "Unknown"

handle("train 5")         # "Train 5 epochs"
handle("save a.pt b.pt")  # "Save to ['a.pt', 'b.pt']"
handle("train abc")       # "Unknown" (guard thất bại)

# Khớp dict: chỉ cần có các key được liệt kê (key thừa vẫn khớp)
match {"type": "image", "size": 224, "extra": 1}:
    case {"type": "image", "size": s}:
        print(f"Ảnh kích thước {s}")
```

> **Bẫy:** `case x:` (tên biến trần) **luôn khớp** và gán giá trị vào `x`; nó **không** so sánh với biến `x` có sẵn bên ngoài. Muốn so sánh với một hằng số, hãy dùng giá trị trực tiếp (`case 0:`) hoặc tên có dấu chấm (`case Color.RED:`).

---

## Thực hành

Mở [exercises.py](./exercises.py), hoàn thành các hàm `# TODO` và chạy kiểm tra:
```bash
python3 01_python_core_and_slicing/exercises.py
```

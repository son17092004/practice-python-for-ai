# Module 05: File I/O, JSON/CSV, Exceptions, Modules & Môi trường (Chi tiết)

---

## 1. `pathlib.Path`: Làm việc với đường dẫn hiện đại

Thay vì dùng `os.path.join` dài dòng, Python 3 dùng `pathlib.Path`:

```python
from pathlib import Path

p = Path("datasets/nlp/train.jsonl")
p.name       # "train.jsonl"
p.stem       # "train"
p.suffix     # ".jsonl"
p.parent     # Path("datasets/nlp")

# Nối đường dẫn bằng dấu /
out = Path("outputs") / "run_01" / "metrics.json"
out.parent.mkdir(parents=True, exist_ok=True)  # Tạo thư mục cha an toàn, không lỗi nếu đã có

# Tìm tất cả file .jsonl trong thư mục (dùng rglob để tìm đệ quy cả thư mục con)
for file in Path("datasets").rglob("*.jsonl"):
    print(file)
```

---

## 2. File I/O & Context Manager (`with`)

Luôn mở file bằng `with` để Python **tự động đóng file** ngay cả khi có lỗi xảy ra bên trong.

| Mode | Ý nghĩa |
| :--- | :--- |
| `"r"` | Đọc text (mặc định). Báo `FileNotFoundError` nếu không có file. |
| `"w"` | Ghi text (ghi đè toàn bộ nội dung cũ hoặc tạo mới). |
| `"a"` | Ghi nối tiếp vào cuối file (append). |
| `"rb"` / `"wb"` | Đọc / ghi nhị phân (ảnh, model weights `.pt`, `pickle`). |

```python
# Đọc file lớn từng dòng (KHÔNG tốn RAM load cả file vào bộ nhớ)
with open("sample_data.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        process(line.strip())
```

### Tự viết Context Manager (Câu hay gặp trong bài test!)
```python
from contextlib import contextmanager
import time

@contextmanager
def timer_context(label: str):
    t0 = time.perf_counter()
    try:
        yield   # Code bên trong khối `with` sẽ chạy tại đây
    finally:
        print(f"[{label}] xong trong {time.perf_counter() - t0:.4f}s")

with timer_context("Load Data"):
    sum(range(100_000))
```

### Context Manager dạng class: `__enter__` / `__exit__`
Câu lệnh `with X() as v:` thực chất là:
1. Gọi `X().__enter__()`; giá trị trả về được gán cho `v`.
2. Chạy thân khối `with`.
3. **Luôn** gọi `__exit__(exc_type, exc_value, traceback)`, kể cả khi thân khối có lỗi. Nếu không có lỗi, cả 3 tham số đều là `None`.

```python
import time

class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self                       # để dùng được `with Timer() as t:`

    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self.start
        return False                      # False/None = KHÔNG nuốt lỗi, lỗi vẫn được ném ra ngoài

with Timer() as t:
    sum(range(100_000))
print(f"{t.elapsed:.4f}s")
```

> **Bẫy:** Nếu `__exit__` trả về `True`, mọi exception trong khối `with` sẽ bị **nuốt mất** một cách im lặng. Chỉ làm vậy khi bạn thực sự muốn bỏ qua lỗi.
>
> **Góc nhìn AI:** `with torch.no_grad():`, `with torch.autocast("cuda"):` và `with open(...)` đều là context manager: vào khối thì bật một chế độ, ra khối thì tự khôi phục lại.

---

## 3. JSON, JSONL & CSV

- **JSON**: `json.load(f)` / `json.dump(obj, f)` (với file), `json.loads(s)` / `json.dumps(obj)` (với chuỗi). Luôn thêm `ensure_ascii=False` khi có tiếng Việt!
- **JSONL (JSON Lines)**: Mỗi dòng là một JSON object. Chuẩn lưu dữ liệu train/fine-tune LLM.
- **CSV**: Dùng module `csv` tích hợp sẵn (trước khi chuyển sang Pandas):
  ```python
  import csv
  with open("data.csv", "r", encoding="utf-8") as f:
      reader = csv.DictReader(f)   # Mỗi dòng là một dict theo tên cột!
      for row in reader:
          print(row["text"], row["label"])
  ```

---

## 4. Xử lý Ngoại lệ: `try / except / else / finally`

Hiểu đúng thứ tự chạy của 4 khối này là kiến thức bắt buộc trong mọi bài test Python:

```python
try:
    # Code có khả năng gây lỗi
    val = int("123")
except ValueError as e:
    # Chạy khi CÓ lỗi ValueError
    print(f"Lỗi chuyển đổi: {e}")
else:
    # CHỈ chạy khi khối `try` KHÔNG có bất kỳ lỗi nào
    print("Thành công:", val)
finally:
    # LUÔN LUÔN chạy dù có lỗi hay không (kể cả khi có `return`!)
    print("Dọn dẹp tài nguyên")
```

**Thứ tự in ra** của khối trên: `Thành công: 123`, rồi `Dọn dẹp tài nguyên`. Nếu thay `"123"` bằng `"abc"`: `Lỗi chuyển đổi: ...`, rồi `Dọn dẹp tài nguyên` (khối `else` bị bỏ qua).

**Các quy tắc cần nhớ thêm:**
- Python xét các khối `except` **từ trên xuống** và chỉ chạy khối **đầu tiên khớp**. Vì vậy hãy đặt exception **cụ thể trước, tổng quát sau**. Nếu đặt `except Exception` lên đầu, nó sẽ chặn hết và các `except ValueError` bên dưới không bao giờ chạy.
- Bắt nhiều loại trong một khối: `except (ValueError, KeyError) as e:`.
- Tránh dùng `except:` trần: nó bắt cả `KeyboardInterrupt` (Ctrl+C), khiến bạn không dừng được chương trình.
- `raise` (không có gì phía sau) trong khối `except` dùng để **ném lại** lỗi đang xử lý. `raise NewError(...) from e` dùng để bọc lỗi gốc vào một lỗi mới mà vẫn giữ nguyên traceback.
- Vì sao cần `else` khi có thể viết luôn vào `try`? Để khối `try` chỉ chứa **đúng** dòng có thể lỗi; code đặt trong `else` nếu có lỗi sẽ không bị `except` phía trên vô tình bắt nhầm.

### Tạo Custom Exception
```python
class DatasetError(Exception):
    """Lỗi riêng cho pipeline dữ liệu."""
    pass

def validate_sample(sample: dict):
    if "text" not in sample:
        raise DatasetError("Thiếu trường 'text' bắt buộc")
```

---

## 5. Module, Package & `if __name__ == "__main__":`

- Khi chạy trực tiếp `python3 my_script.py`, biến đặc biệt `__name__` có giá trị `"__main__"`.
- Khi file đó được `import` từ một file khác, `__name__` sẽ là tên của file (ví dụ `"my_script"`).
- Vì vậy, luôn đặt code chạy thử / test vào trong `if __name__ == "__main__":` để khi `import` hàm từ file đó sang nơi khác, code chạy thử không tự động kích hoạt.

---

## 6. Quản lý Môi trường ảo (`uv` / `venv`)

Các dự án AI thường yêu cầu phiên bản thư viện khác nhau (ví dụ PyTorch + CUDA). Luôn tách môi trường riêng:

```bash
# Dùng uv (siêu nhanh, đã cài sẵn trên máy của bạn):
uv venv
source .venv/bin/activate
uv pip install numpy pandas scikit-learn torch

# Hoặc dùng venv chuẩn của Python:
python3 -m venv .venv
source .venv/bin/activate
```

---

## Thực hành

Mở [exercises.py](./exercises.py) và chạy kiểm tra:
```bash
python3 05_files_json_and_environments/exercises.py
```

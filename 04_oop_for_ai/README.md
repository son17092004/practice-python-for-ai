# Module 04: Lập trình Hướng đối tượng (OOP) & Kiến trúc AI (Chi tiết)

OOP là phần gần như **chắc chắn có** trong các bài test Python và là nền tảng bắt buộc để viết code **PyTorch** (`Dataset`, `nn.Module`), **Scikit-learn** (`fit`/`predict`) hay **LangChain**.

---

## 1. Class Attribute vs Instance Attribute (Bẫy Test Kinh Điển!)

```python
class Model:
    framework = "PyTorch"   # Class attribute: dùng chung cho MỌI object
    all_layers = []         # CẨN THẬN nếu class attribute là mutable (list/dict)!

    def __init__(self, name: str):
        self.name = name    # Instance attribute: riêng của từng object

m1 = Model("ResNet")
m2 = Model("ViT")

# Nếu gán m1.framework = "JAX":
# Python TẠO MỘT instance attribute mới trên m1, KHÔNG sửa Model.framework!
m1.framework = "JAX"
print(m1.framework, m2.framework)  # "JAX", "PyTorch"

# NHƯNG nếu mutate list class attribute:
m1.all_layers.append("Conv2d")
print(m2.all_layers)               # ["Conv2d"] -> m2 bị dính theo!
```
**Quy tắc vàng:** Các thuộc tính riêng (đặc biệt là `list`, `dict`) luôn khởi tạo bên trong `__init__` với `self.`.

---

## 2. Ba loại Method & `@property`

| Loại | Decorator | Tham số đầu | Dùng khi nào? |
| :--- | :--- | :--- | :--- |
| **Instance method** | (không có) | `self` | Thao tác với dữ liệu của từng object (`model.forward(x)`) |
| **Class method** | `@classmethod` | `cls` | Tạo factory constructor (ví dụ: `Model.from_config(cfg)`, `AutoModel.from_pretrained(...)`) |
| **Static method** | `@staticmethod` | (không có) | Hàm tiện ích liên quan logic của class nhưng không cần `self` hay `cls` |

### `@property`: Kiểm soát truy cập thuộc tính như biến bình thường
```python
class LearningRate:
    def __init__(self, value: float):
        self._value = value

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, new_val: float):
        if new_val <= 0:
            raise ValueError("Learning rate phải > 0")
        self._value = new_val

lr = LearningRate(1e-3)
print(lr.value)   # Gọi như thuộc tính, không cần dấu ()
lr.value = -1     # Gọi setter -> ValueError
```

**`@property` không có setter thì thuộc tính là CHỈ ĐỌC (read-only)**. Đây là cách tạo "thuộc tính tính toán" luôn đúng theo dữ liệu hiện tại:

```python
class Batch:
    def __init__(self, items: list):
        self.items = items

    @property
    def size(self) -> int:       # luôn tính lại từ items, không bao giờ bị lệch
        return len(self.items)

b = Batch([1, 2, 3])
b.items.append(4)
b.size        # 4
b.size = 10   # AttributeError: property 'size' ... has no setter
```

---

## 3. Kế thừa, `super()` & MRO

```python
class BaseLayer:
    def __init__(self, name: str):
        self.name = name

    def forward(self, x):
        raise NotImplementedError("Lớp con phải cài đặt forward()")

class Linear(BaseLayer):
    def __init__(self, name: str, weight: float):
        super().__init__(name)   # Luôn gọi super().__init__() để khởi tạo lớp cha!
        self.weight = weight

    def forward(self, x: float) -> float:
        return x * self.weight
```

- **Kiểm tra quan hệ:** `isinstance(obj, BaseLayer)` trả về `True` (kể cả với lớp con); `issubclass(Linear, BaseLayer)` trả về `True`.
- **Đa kế thừa & MRO (Method Resolution Order):** Khi kế thừa nhiều lớp `class C(A, B):`, Python tìm method theo thuật toán C3 Linearization (trái sang phải, sâu trước khi lên cha chung). Có thể kiểm tra bằng `C.__mro__`.

### Abstract Base Class (`abc`): ép lớp con phải cài đặt method

Cách `raise NotImplementedError` ở trên chỉ báo lỗi **khi gọi** `forward()`. Dùng `ABC` + `@abstractmethod` thì Python báo lỗi **ngay khi tạo object** từ một lớp con thiếu method:

```python
from abc import ABC, abstractmethod

class BaseLayer(ABC):
    @abstractmethod
    def forward(self, x): ...

class Broken(BaseLayer):
    pass                    # quên viết forward

BaseLayer()   # TypeError: Can't instantiate abstract class BaseLayer ...
Broken()      # TypeError: ... without an implementation for abstract method 'forward'
```

> **Góc nhìn AI:** Scikit-learn và LangChain dùng nhiều lớp trừu tượng kiểu này (ví dụ `BaseEstimator`, `BaseRetriever`) để định nghĩa một "hợp đồng" mà mọi lớp con phải tuân theo.

---

## 4. Dunder Methods (Magic Methods) — Trái tim của PyTorch

| Method | Cách Python gọi | Vai trò trong AI (PyTorch / Sklearn) |
| :--- | :--- | :--- |
| `__init__` | `MyClass()` | Khởi tạo layers, đọc danh sách file dữ liệu |
| `__repr__` | `repr(obj)` / debug | Hiển thị kiến trúc model rõ ràng (`Linear(in=10, out=5)`) |
| `__str__` | `print(obj)` | Chuỗi thân thiện cho người dùng (nếu không có `__str__`, dùng `__repr__`) |
| `__len__` | `len(dataset)` | Trả về tổng số mẫu dữ liệu (`torch.utils.data.Dataset`) |
| `__getitem__` | `dataset[idx]` | Lấy mẫu `(x, y)` thứ `idx` (`Dataset` & slicing) |
| `__call__` | `model(x)` | Biến object thành callable — `nn.Module.__call__` gọi `forward(x)` + chạy hooks |
| `__eq__` | `a == b` | So sánh 2 config hoặc 2 object theo giá trị |

### Ví dụ mô phỏng `nn.Module`:
```python
class BaseModule:
    def __call__(self, x):
        return self.forward(x)

    def forward(self, x):
        raise NotImplementedError

class ReLU(BaseModule):
    def forward(self, x: list[float]) -> list[float]:
        return [max(0.0, v) for v in x]

relu = ReLU()
print(relu([-2.0, 3.0]))  # Gọi __call__ -> tự động gọi forward() -> [0.0, 3.0]
```

---

## 5. `@dataclass` (Quản lý Config & Data Model hiện đại)

`@dataclass` tự động sinh `__init__`, `__repr__`, `__eq__` giúp code cực gọn:

```python
from dataclasses import dataclass, field

@dataclass
class TrainingConfig:
    learning_rate: float = 3e-4
    batch_size: int = 32
    epochs: int = 10
    # BẪY: Không viết `tags: list[str] = []` trong dataclass!
    # Phải dùng `field(default_factory=list)` để mỗi instance có list riêng:
    tags: list[str] = field(default_factory=list)

# Có thể thêm `frozen=True` vào `@dataclass(frozen=True)` để biến object thành immutable!
```

---

## 6. Tự viết class duyệt được bằng `for` (`__iter__` / `__next__`)

Nhắc lại từ Module 02 (§9): `for x in obj` sẽ gọi `iter(obj)` → `obj.__iter__()`, rồi gọi `next()` liên tục cho đến khi gặp `StopIteration`. Có 2 cách để class của bạn hỗ trợ `for`:

**Cách 1: `__iter__` là generator (dùng `yield`). Đây là cách nên dùng.** Mỗi vòng `for` tạo một generator mới, nên object **duyệt lại được nhiều lần**:

```python
class Corpus:
    def __init__(self, texts: list[str]):
        self.texts = texts

    def __iter__(self):
        for t in self.texts:
            yield t.lower()

c = Corpus(["A", "B"])
list(c)   # ['a', 'b']
list(c)   # ['a', 'b']  -> duyệt lại vẫn được!
```

**Cách 2: tự viết `__next__` (iterator thủ công).** Object tự lưu vị trí hiện tại, nên **chỉ duyệt được 1 lần**, giống generator:

```python
class Countdown:
    def __init__(self, start: int):
        self.current = start

    def __iter__(self):
        return self              # iterator trả về chính nó

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration  # báo hiệu hết
        self.current -= 1
        return self.current + 1

list(Countdown(3))   # [3, 2, 1]
```

> **Góc nhìn AI:** `torch.utils.data.DataLoader` thuộc Cách 1: nó là iterable, và mỗi epoch `for batch in loader:` lại tạo một iterator mới (và shuffle lại nếu `shuffle=True`). Trong bài tập, bạn sẽ tự viết `MiniDataLoader` theo đúng mô hình này.

---

## Thực hành

Mở [exercises.py](./exercises.py) và chạy kiểm tra:
```bash
python3 04_oop_for_ai/exercises.py
```

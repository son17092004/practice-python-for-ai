# Module 07: Xử lý Văn bản: Regex, Unicode & Ngẫu nhiên có kiểm soát (Chi tiết)

Trong NLP và LLM, **phần lớn thời gian là làm sạch dữ liệu văn bản**. Module này trang bị 3 công cụ mà các module trước chưa dạy, nhưng bạn sẽ dùng hằng ngày:

1. **Regex (`re`)**: tìm, trích xuất, thay thế văn bản theo mẫu (Capstone dùng nó trong `tokenize()`).
2. **Unicode**: xử lý tiếng Việt đúng cách (`str` và `bytes`, chuẩn hóa NFC/NFD, bỏ dấu).
3. **`random` & seed**: shuffle và chia dữ liệu sao cho **chạy lại ra đúng kết quả cũ** (reproducibility).

---

## 1. Regular Expression (`re`)

### 1.1. Luôn dùng raw string `r"..."`
Trong chuỗi thường, `\b` là ký tự backspace và `\n` là xuống dòng. Viết `r"\b\d+"` thì Python giữ nguyên dấu `\` để `re` tự hiểu. **Quy tắc: mọi pattern regex đều viết với tiền tố `r`.**

### 1.2. Bảng cú pháp cần thuộc

| Ký hiệu | Ý nghĩa | Ví dụ khớp |
| :--- | :--- | :--- |
| `.` | Một ký tự bất kỳ (trừ xuống dòng) | `a.c` khớp `abc`, `a-c` |
| `\d` / `\D` | Chữ số / không phải chữ số | `\d\d` khớp `42` |
| `\w` / `\W` | Ký tự "chữ" (chữ cái **mọi ngôn ngữ**, số, `_`) / ngược lại | `\w+` khớp `việt` |
| `\s` / `\S` | Khoảng trắng (space, tab, `\n`) / ngược lại | `\s+` khớp `"   \n"` |
| `[abc]` / `[^abc]` / `[a-z]` | Một ký tự trong tập / ngoài tập / trong khoảng | `[0-9a-f]` khớp chữ số hex |
| `^` / `$` | Đầu / cuối chuỗi | `^Epoch` |
| `\b` | Ranh giới từ | `\bai\b` khớp `ai` nhưng không khớp `email` |
| `*` / `+` / `?` | 0+ lần / 1+ lần / 0 hoặc 1 lần | `colou?r` khớp `color`, `colour` |
| `{m}` / `{m,n}` | Đúng m lần / từ m đến n lần | `\d{4}` khớp `2024` |
| `a\|b` | a hoặc b | `cat\|dog` |
| `( )` | Nhóm (group): bắt lấy phần khớp | `(\d+)/(\d+)` |
| `(?P<ten>...)` | Nhóm có tên | `(?P<day>\d+)` |
| `\.` `\(` `\?` … | Ký tự đặc biệt dạng **chữ thường** (escape) | `\.` khớp đúng dấu chấm |

### 1.3. Các hàm chính

```python
import re
text = "Liên hệ an@example.com hoặc hotline 0901-234-567 trước 25/12"

re.findall(r"\d+", text)              # ['0901', '234', '567', '25', '12'] -> list mọi chuỗi khớp
re.findall(r"\w+@\w+\.\w+", text)     # ['an@example.com']
re.search(r"\d{4}-\d{3}-\d{3}", text).group()   # '0901-234-567' -> Match object ĐẦU TIÊN (hoặc None)
re.sub(r"\s+", " ", "  quá   nhiều \n khoảng trắng ").strip()   # 'quá nhiều khoảng trắng'
re.split(r"[,;]\s*", "a, b;c,  d")    # ['a', 'b', 'c', 'd']
re.findall(r"python", "Python PYTHON", flags=re.IGNORECASE)    # ['Python', 'PYTHON']

# Dùng một pattern nhiều lần (ví dụ trong vòng lặp qua hàng triệu dòng) -> compile 1 lần:
DIGITS = re.compile(r"\d+")
DIGITS.findall("a1b22")               # ['1', '22']
```

### 1.4. Bẫy `match` / `search` / `fullmatch` (Hay ra trong test!)

```python
re.match(r"\d+", "abc123")      # None  -> match CHỈ thử khớp ở ĐẦU chuỗi!
re.search(r"\d+", "abc123")     # <Match '123'> -> search tìm ở BẤT KỲ đâu
re.fullmatch(r"\d+", "123x")    # None  -> fullmatch đòi khớp TOÀN BỘ chuỗi (dùng để validate)
```

> **Luôn kiểm tra `None`** trước khi gọi `.group()`: `if (m := re.search(...)) is not None:`. Đây là chỗ walrus (Module 01) phát huy tác dụng.

### 1.5. Group & Named group

```python
m = re.search(r"(\d+)/(\d+)", text)
m.group(0), m.group(1), m.groups()    # ('25/12', '25', ('25', '12'))  -> group(0) = cả chuỗi khớp

m = re.search(r"(?P<day>\d+)/(?P<month>\d+)", text)
m["day"], m.groupdict()               # ('25', {'day': '25', 'month': '12'})

re.sub(r"(\d+)/(\d+)", r"\2-\1", "25/12")   # '12-25' -> \1, \2 tham chiếu lại group
```

> **Bẫy `findall` + group:** Nếu pattern có group, `findall` trả về **nội dung group**, không phải cả chuỗi khớp:
> `re.findall(r"(\d+)/(\d+)", "1/2 và 3/4")` cho ra `[('1', '2'), ('3', '4')]`.
> Muốn nhóm lại mà **không bắt**, dùng non-capturing group `(?:...)`.

### 1.6. Greedy và non-greedy

```python
re.findall(r"<.*>", "<b>đậm</b>")     # ['<b>đậm</b>']  -> * "tham lam": nuốt dài nhất có thể
re.findall(r"<.*?>", "<b>đậm</b>")    # ['<b>', '</b>'] -> *? lấy ngắn nhất có thể
```

### 1.7. Regex và tiếng Việt

```python
re.findall(r"[a-z0-9]+", "học máy 2024")        # ['h', 'c', 'm', 'y', '2024']  -> HỎNG!
re.findall(r"\w+", "Học máy 2024!".lower())     # ['học', 'máy', '2024']       -> đúng
```

`[a-z]` chỉ gồm 26 chữ cái Latin không dấu. Trong Python 3, `\w` hiểu Unicode nên giữ được chữ có dấu. Hàm `tokenize()` của Capstone dùng `[a-z0-9]+`, nên **không dùng được cho tiếng Việt**. Bạn sẽ sửa điều này trong bài tập.

---

## 2. Unicode: `str`, `bytes` & tiếng Việt

### 2.1. `str` và `bytes`
- `str`: chuỗi các **ký tự Unicode** (thứ bạn thấy).
- `bytes`: chuỗi các **byte thô** (thứ được lưu trên đĩa hoặc gửi qua mạng).
- `str.encode("utf-8")` cho ra `bytes`; `bytes.decode("utf-8")` cho ra lại `str`.

```python
s = "việt"
len(s)                    # 4 ký tự
b = s.encode("utf-8")     # b'vi\xe1\xbb\x87t'
len(b)                    # 6 byte  -> chữ 'ệ' chiếm 3 byte trong UTF-8
b.decode("utf-8")         # 'việt'
b.decode("ascii")         # UnicodeDecodeError: 'ascii' codec can't decode byte 0xe1 ...
```

> **Quy tắc:** luôn mở file văn bản với `encoding="utf-8"` (Module 05). Nếu không chỉ định, Python dùng encoding mặc định của hệ điều hành (trên Windows thường không phải UTF-8), và đó là nguồn gốc của rất nhiều lỗi `UnicodeDecodeError`.

### 2.2. Bẫy NFC và NFD: hai chữ "giống hệt nhau" nhưng `==` lại `False`

Cùng một chữ `ệ` có thể được lưu theo 2 cách:
- **NFC (dựng sẵn):** 1 ký tự `U+1EC7`.
- **NFD (tổ hợp):** 3 ký tự: `e` + dấu nặng `U+0323` + dấu mũ `U+0302`.

```python
import unicodedata
nfc = unicodedata.normalize("NFC", "việt")
nfd = unicodedata.normalize("NFD", "việt")
nfc == nfd               # False !!
len(nfc), len(nfd)       # (4, 6)
unicodedata.normalize("NFC", nfd) == nfc   # True -> chuẩn hóa xong mới so sánh
```

Văn bản dạng NFD hay gặp khi: tên file trên macOS, copy từ một số trang web/PDF, gõ bằng chế độ "Unicode tổ hợp". Nếu không chuẩn hóa, cùng một từ sẽ thành **2 token khác nhau** trong vocab, và tìm kiếm sẽ không thấy kết quả.

> **Quy tắc NLP tiếng Việt:** bước đầu tiên của mọi pipeline làm sạch là `unicodedata.normalize("NFC", text)`.

### 2.3. Bỏ dấu tiếng Việt

Mẹo: chuyển sang NFD để tách dấu thành ký tự riêng, rồi lọc bỏ các ký tự dấu (`unicodedata.combining(c)` khác 0):

```python
s = unicodedata.normalize("NFD", "Tiếng Việt Đẹp")
"".join(c for c in s if not unicodedata.combining(c))   # 'Tieng Viet Đep'  -> còn sót 'Đ'!
```

`đ`/`Đ` là **chữ cái riêng**, không phải `d` cộng thêm dấu, nên NFD không tách được. Phải thay thủ công: `.replace("đ", "d").replace("Đ", "D")`.

### 2.4. `lower()` và `casefold()`
`casefold()` mạnh hơn `lower()`, dùng khi so sánh không phân biệt hoa thường với nhiều ngôn ngữ: `"Straße".lower()` cho `'straße'`, còn `"Straße".casefold()` cho `'strasse'`.

---

## 3. Ngẫu nhiên có kiểm soát: `random` & seed

### 3.1. Các hàm hay dùng và bẫy đi kèm

```python
import random

random.random()                 # float trong [0.0, 1.0)
random.randint(1, 6)            # số nguyên trong [1, 6]: BAO GỒM CẢ 6 (khác với range!)
random.choice(["a", "b", "c"])  # 1 phần tử
random.choices(["a", "b"], weights=[0.9, 0.1], k=5)  # 5 phần tử, CÓ lặp lại, theo trọng số
random.sample(range(100), k=5)  # 5 phần tử KHÔNG lặp lại

data = [1, 2, 3, 4]
result = random.shuffle(data)   # BẪY: shuffle xáo TẠI CHỖ và trả về None!
print(result)                   # None
print(data)                     # [3, 1, 4, 2] (ví dụ) -> data gốc đã bị thay đổi
```

### 3.2. Seed: để "ngẫu nhiên" mà vẫn lặp lại được

Máy tính sinh số **giả ngẫu nhiên** từ một giá trị khởi đầu gọi là **seed**. Cùng seed thì cùng một dãy số:

```python
random.seed(42); a = [random.random() for _ in range(3)]
random.seed(42); b = [random.random() for _ in range(3)]
a == b    # True

# CÁCH TỐT HƠN: tạo bộ sinh số riêng, không đụng tới trạng thái toàn cục
rng = random.Random(42)
rng.random()        # 0.6394267984578837 (luôn ra số này với seed 42)
rng.shuffle(data)   # xáo bằng rng riêng
```

`random.seed()` toàn cục có thể bị **thư viện khác** gọi lại và làm xáo trộn dãy số của bạn. `random.Random(seed)` là một object độc lập, nên an toàn hơn và dễ test hơn.

### 3.3. Góc nhìn AI: Reproducibility

Kết quả training phụ thuộc vào thứ tự dữ liệu, cách khởi tạo trọng số, dropout… tất cả đều là "ngẫu nhiên". Muốn người khác (hoặc chính bạn tuần sau) chạy lại ra **cùng kết quả**, phải đặt seed ở **mọi** thư viện:

| Thư viện | Cách đặt seed |
| :--- | :--- |
| Python | `random.seed(42)` hoặc `random.Random(42)` |
| NumPy | `rng = np.random.default_rng(42)` |
| PyTorch | `torch.manual_seed(42)` (và `torch.cuda.manual_seed_all(42)` cho GPU) |
| HuggingFace | `transformers.set_seed(42)`: đặt seed cho cả 3 thư viện trên |

**Chia train/test đúng cách:**
1. **Copy** dữ liệu trước khi shuffle (đừng làm hỏng dữ liệu gốc, xem Module 01).
2. **Shuffle bằng seed cố định**: nếu dữ liệu đang được sắp theo nhãn hoặc theo thời gian mà không shuffle, tập test sẽ lệch hoàn toàn.
3. **Rồi mới slice**.

---

## Thực hành

Mở [exercises.py](./exercises.py), hoàn thành các hàm `# TODO` và chạy kiểm tra:
```bash
python3 07_text_regex_and_randomness/exercises.py
```

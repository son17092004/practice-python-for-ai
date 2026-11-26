# Khóa Học Ôn Tập Python Hướng AI — Hướng Dẫn Tự Học

Khóa học dành cho người **đã từng học Python nhưng đã quên**, muốn ôn lại nhanh, đúng trọng tâm để bước vào **Machine Learning / Deep Learning / LLM**.

**Sau khóa học, bạn sẽ:**
- Tránh được các bẫy kinh điển trong bài test Python đầu vào (mutability, `is` và `==`, slicing, `round()`, closure, class attribute, iterator, thứ tự `except`…).
- Viết được code Python hiện đại (3.10+): comprehension, generator, type hint, decorator, dataclass.
- Hiểu bản chất các thành phần mà PyTorch/HuggingFace dùng hằng ngày: `Dataset`, `nn.Module`, JSONL, softmax, cosine similarity.
- Làm sạch văn bản tiếng Việt bằng regex và Unicode, đồng thời chia dữ liệu sao cho chạy lại ra đúng kết quả (seed).
- Tự xây được một mini search engine (nền tảng của RAG) bằng Python thuần.

> Toàn bộ khóa học chỉ dùng **thư viện chuẩn của Python**, không cần cài thêm gói nào.

---

## Mục lục

0. [Chuẩn bị trước khi học](#0-chuẩn-bị-trước-khi-học)
1. [Cấu trúc thư mục: file nào dùng để làm gì?](#1-cấu-trúc-thư-mục-file-nào-dùng-để-làm-gì)
2. [Bản đồ khóa học & thời lượng](#2-bản-đồ-khóa-học--thời-lượng)
3. [Quy trình học MỘT module (7 bước)](#3-quy-trình-học-một-module-7-bước)
4. [Đọc hiểu kết quả khi chạy bài tập](#4-đọc-hiểu-kết-quả-khi-chạy-bài-tập)
5. [Khi bị kẹt: thang gợi ý 4 nấc](#5-khi-bị-kẹt-thang-gợi-ý-4-nấc)
6. [Hướng dẫn riêng cho từng module](#6-hướng-dẫn-riêng-cho-từng-module)
7. [Capstone: cách học một project có sẵn code](#7-capstone-cách-học-một-project-có-sẵn-code)
8. [Bài test thử (Mock Test)](#8-bài-test-thử-mock-test)
9. [Lịch học gợi ý](#9-lịch-học-gợi-ý)
10. [Bảng theo dõi tiến độ](#10-bảng-theo-dõi-tiến-độ)
11. [Bước tiếp theo sau khóa học](#11-bước-tiếp-theo-sau-khóa-học)

---

## 0. Chuẩn bị trước khi học

### 0.1. Kiểm tra phiên bản Python (bắt buộc ≥ 3.10)

```bash
python3 --version
```

Bài tập dùng cú pháp `float | None` và `list[int]`. Với Python < 3.10, bạn sẽ gặp `TypeError: unsupported operand type(s) for |` ngay khi chạy file, dù chưa viết dòng code nào. Khi đó hãy cài Python mới hơn, chẳng hạn bằng `uv python install 3.12`.

### 0.2. Luôn đứng ở thư mục gốc của khóa học

Mọi lệnh trong hướng dẫn này đều chạy từ **thư mục chứa file README này**:

```bash
cd /đường/dẫn/tới/Python      # thư mục chứa README.md, mock_entry_test.py
ls                             # phải thấy 01_python_core_and_slicing/, 02_..., capstone_..., mock_entry_test.py
```

Nếu gặp `can't open file '...exercises.py': [Errno 2] No such file or directory`, nghĩa là bạn đang đứng sai thư mục.

### 0.3. Công cụ

- **Một trình soạn thảo** (VS Code là đủ) để mở `README.md` và sửa `exercises.py`.
- **Một terminal** để chạy lệnh.
- **Python REPL** để thử nhanh: gõ `python3` trong terminal, gõ `exit()` hoặc nhấn `Ctrl+D` để thoát. Đây là công cụ học quan trọng nhất (xem [Bước 2](#bước-2--đọc-chủ-động-readme-có-gõ-có-chạy)).

### 0.4. Sao lưu bài tập trống (khuyến nghị)

Bạn sẽ ghi đè lên `exercises.py` khi làm bài. Hãy giữ một bản trống để **làm lại lần 2** sau vài ngày, vì làm lại là cách nhớ lâu nhất:

```bash
for d in 0*/; do cp "$d/exercises.py" "$d/exercises_blank.py"; done
```

---

## 1. Cấu trúc thư mục: file nào dùng để làm gì?

Mỗi module `01` → `07` có đúng 3 file:

| File | Vai trò | Khi nào dùng |
| :--- | :--- | :--- |
| `README.md` | **Lý thuyết**: cú pháp, bẫy hay gặp, "Góc nhìn AI" | Đọc **đầu tiên** |
| `exercises.py` | **Bài tập**: các hàm/lớp có `# TODO` mà bạn phải điền; phần cuối file (`if __name__ == "__main__":`) chứa **test tự động** | Làm **sau khi** đọc README |
| `solutions.py` | **Lời giải tham khảo** | **Chỉ mở** khi đã làm xong, hoặc đã kẹt đúng theo [thang gợi ý](#5-khi-bị-kẹt-thang-gợi-ý-4-nấc) |

Riêng một số module có thêm file phụ:
- `05_.../sample_data.jsonl`: dữ liệu mẫu mà bài tập Module 05 đọc vào. **Đừng sửa file này**, vì test dựa trên nội dung của nó.
- `capstone_mini_rag_search/`: project hoàn chỉnh, xem [mục 7](#7-capstone-cách-học-một-project-có-sẵn-code).
- `mock_entry_test.py`: bài trắc nghiệm tương tác 20 câu, xem [mục 8](#8-bài-test-thử-mock-test).

> ⚠️ **Đừng mở `solutions.py` "chỉ để xem qua".** Khi đã thấy lời giải, não sẽ nhầm "hiểu" thành "biết làm". Giá trị của khóa học nằm ở việc bạn tự vật lộn với bài tập.

---

## 2. Bản đồ khóa học & thời lượng

Học **theo đúng thứ tự**, vì module sau dùng kiến thức của module trước. Thời lượng dưới đây là ước lượng cho người đã từng biết Python.

| # | Chủ đề | Bài tập phải làm | Trọng tâm cho AI | Thời lượng |
| :--- | :--- | :--- | :--- | :--- |
| **01** | [Core Syntax, Mutability & Slicing](./01_python_core_and_slicing/README.md) | `split_train_val_test`, `normalize_matrix_safe`, `sliding_windows`, `format_training_log`, `early_stopping_epoch`, `parse_command` | Chia train/val/test, không sửa nhầm dữ liệu gốc, early stopping | 3–4 giờ |
| **02** | [Data Structures & Comprehensions](./02_data_structures_and_comprehensions/README.md) | `build_vocab`, `encode_sentence`, `batch_generator`, `compute_accuracy`, `top_k_documents`, `take_valid`, `rank_words` | Vocab cho NLP, chia batch, Top-K, xử lý dữ liệu streaming | 3–4 giờ |
| **03** | [Functions, Type Hints & Decorators](./03_functions_typing_and_decorators/README.md) | `append_metric`, `compose_transforms`, `merge_configs`, `count_calls`, `make_scalers`, `make_running_mean`, `flatten_config` | Gộp config, pipeline tiền xử lý, decorator, closure, đệ quy | 3–4 giờ |
| **04** | [OOP cho AI](./04_oop_for_ai/README.md) | `TrainConfig`, `MiniDataset`, `Linear1D`, `ReLU`, `Sequential`, `TrackedModel`, `StepLRScheduler`, `MiniDataLoader` | Bản chất `Dataset`, `DataLoader`, `nn.Module`, LR scheduler | 3–4 giờ |
| **05** | [File I/O, JSONL, Exceptions & `uv`](./05_files_json_and_environments/README.md) | `load_valid_jsonl`, `save_json_summary`, `safe_to_float`, `temporary_setting`, `Timer` | Đọc dữ liệu LLM dạng JSONL, xử lý lỗi, context manager | 2.5–3 giờ |
| **06** | [Vectorization & Toán AI](./06_vectorization_math_to_ai/README.md) | `dot_product`, `cosine_similarity`, `softmax`, `matmul` | 4 phép toán xương sống của mạng neural | 2–3 giờ |
| **07** | [Text: Regex, Unicode & Random](./07_text_regex_and_randomness/README.md) | `clean_text`, `tokenize_vi`, `remove_accents`, `parse_log_line`, `shuffle_split` | Làm sạch văn bản tiếng Việt, đọc log, chia dữ liệu tái lập được | 3–4 giờ |
| **Capstone** | [Mini Search Engine](./capstone_mini_rag_search/README.md) | Đọc hiểu + 2 thử thách mở rộng | Ghép toàn bộ kiến thức thành pipeline RAG | 2–4 giờ |
| **Mock Test** | [20 câu trắc nghiệm](./mock_entry_test.py) | Làm 2 lần (đầu và cuối khóa) | Tổng kiểm tra các bẫy | 30 phút/lần |

**Tổng: khoảng 24–32 giờ.**

---

## 3. Quy trình học MỘT module (7 bước)

Lặp lại đúng 7 bước này cho mỗi module 01 → 07.

### Bước 1 — Đọc lướt đề bài TRƯỚC (5 phút)

Mở `exercises.py` và **chỉ đọc** tên hàm cùng docstring (phần `"""..."""`), chưa code gì cả. Mục đích là để biết mình sắp phải làm gì, nhờ đó lúc đọc lý thuyết bạn sẽ chú ý đúng chỗ.

### Bước 2 — Đọc chủ động README (có gõ, có chạy)

Đừng chỉ đọc. Với **mỗi khối code ví dụ** trong README:

1. **Đoán** kết quả trước (nói ra hoặc ghi ra giấy).
2. **Gõ lại** (không copy-paste) vào REPL `python3` rồi chạy.
3. **So sánh** với dự đoán. Nếu đoán sai, đó chính là kiến thức bạn cần học; hãy đánh dấu lại.
4. **Thử biến tấu**: đổi số, đổi kiểu dữ liệu, cố tình làm sai để xem lỗi trông như thế nào.

Ví dụ với mục "Bẫy tạo ma trận 2D" của Module 01:

```python
>>> g = [[0] * 3] * 3      # đoán trước: g[0][0] = 1 thì g thành gì?
>>> g[0][0] = 1
>>> g
[[1, 0, 0], [1, 0, 0], [1, 0, 0]]
>>> [id(row) for row in g]  # biến tấu: kiểm tra 3 hàng có cùng id không
```

Ghi chú các **bẫy** mà bạn đoán sai vào một file riêng (ví dụ `notes.md`). File này là tài liệu ôn thi quý nhất của bạn.

### Bước 3 — Đọc phần test ở cuối `exercises.py`

Kéo xuống khối `if __name__ == "__main__":`. Mỗi dòng `assert` là **một yêu cầu chính xác** mà hàm của bạn phải thỏa mãn. Nhiều khi đọc test còn rõ hơn đọc docstring, ví dụ:

```python
assert sliding_windows([1, 2], 3) == []   # => window lớn hơn dãy thì trả về list rỗng
```

### Bước 4 — Làm TỪNG hàm một, chạy sau mỗi hàm

1. Xóa dòng `pass` rồi viết code thay vào chỗ `# TODO`.
2. **Chạy ngay** sau khi viết xong một hàm:
   ```bash
   python3 01_python_core_and_slicing/exercises.py
   ```
3. Test chạy **theo thứ tự từ trên xuống** và **dừng ở lỗi đầu tiên**. Vì vậy hãy làm các hàm theo thứ tự trong file. Khi hàm 1 đúng, lỗi sẽ "nhảy" xuống hàm 2, và đó là dấu hiệu bạn đang tiến bộ.
4. Không hiểu lỗi? Xem [mục 4](#4-đọc-hiểu-kết-quả-khi-chạy-bài-tập).

**Mẹo: thử riêng một hàm trong REPL** (không cần đợi cả file pass):

```bash
cd 01_python_core_and_slicing
python3
```
```python
>>> from exercises import sliding_windows
>>> sliding_windows([1, 2, 3, 4, 5], 3)
>>> sliding_windows([1, 2], 3)
>>> sliding_windows([1, 2, 3], 0)     # tự nghĩ thêm trường hợp biên
```

> Sau khi **sửa file**, bạn phải thoát REPL (`exit()`) rồi mở lại thì code mới được nạp.

**Mẹo: dùng `python3 -i`** để sau khi chạy (kể cả khi lỗi) bạn vẫn ở lại REPL và gọi hàm để điều tra:

```bash
python3 -i 01_python_core_and_slicing/exercises.py
```

### Bước 5 — Khi tất cả test PASS

Bạn sẽ thấy dòng thông báo ở cuối, ví dụ:

```
Module 01: Tất cả bài test đã PASS!
```

Không có dòng này nghĩa là chưa xong.

### Bước 6 — So sánh với `solutions.py` (chỉ SAU khi PASS)

Đặt code của bạn và `solutions.py` cạnh nhau rồi tự hỏi:
- Lời giải có xử lý **trường hợp biên** mà mình bỏ sót không (list rỗng, chia cho 0, `None`)?
- Lời giải có ngắn gọn hơn nhờ comprehension, `zip`, `Counter`, slicing… không?
- Có hàm nào mình viết bằng vòng lặp dài nhưng lời giải chỉ cần 1–2 dòng?

Nếu thấy cách hay hơn, **tự viết lại** theo cách đó (đừng copy) rồi chạy lại test.

### Bước 7 — Tự kiểm tra trước khi sang module mới

Chỉ chuyển module khi bạn trả lời **"có"** cho cả 3 câu:

- [ ] Test của module in ra dòng `PASS`.
- [ ] Gập README lại, mình vẫn **giải thích được bằng lời** các bẫy chính của module (xem [mục 6](#6-hướng-dẫn-riêng-cho-từng-module)).
- [ ] Mình hiểu vì sao lời giải trong `solutions.py` đúng, kể cả những dòng khác với code của mình.

---

## 4. Đọc hiểu kết quả khi chạy bài tập

Đọc traceback **từ dưới lên**: dòng cuối là **loại lỗi**, dòng `File "...", line N` ngay trên đó cho biết **test nào** đang fail.

| Bạn thấy | Nghĩa là | Cách xử lý |
| :--- | :--- | :--- |
| `TypeError: cannot unpack non-iterable NoneType object` | Hàm vẫn trả về `None`: **chưa làm** hoặc **quên `return`** | Đây là trạng thái bình thường lúc mới bắt đầu. Viết code và nhớ `return` |
| `AssertionError` (không kèm chữ) | Hàm chạy được nhưng **kết quả sai**, hoặc hàm **chưa làm** (vẫn trả về `None`) | Xem dòng `assert` bị báo, gọi hàm đó trong REPL với đúng input ấy và so với kết quả mong đợi |
| `TypeError: ...__init__() got an unexpected keyword argument` | Class chưa khai báo trường/tham số đó (thường gặp ở Module 04 khi chưa làm `TrainConfig`) | Khai báo đủ các trường theo docstring |
| `AssertionError: Không được mutate ma trận gốc!` | Test có kèm thông điệp, hãy đọc kỹ | Ở đây là bạn đã sửa trực tiếp dữ liệu đầu vào, cần tạo list mới |
| `NameError: name 'x' is not defined` | Gõ sai tên biến hoặc dùng biến chưa khai báo | Kiểm tra chính tả |
| `IndentationError` | Thụt lề sai (trộn tab và space, hoặc thiếu thụt lề) | Dùng 4 dấu cách; trong VS Code bật "Render Whitespace" để nhìn rõ |
| `SyntaxError` | Sai cú pháp: thiếu `:`, thiếu ngoặc… | Xem dấu `^` chỉ vị trí lỗi |
| `TypeError: unsupported operand type(s) for \|` | Python < 3.10 | Xem [mục 0.1](#01-kiểm-tra-phiên-bản-python-bắt-buộc--310) |
| `ZeroDivisionError` | Chưa xử lý trường hợp chia cho 0 | Đọc lại docstring: thường có quy định riêng cho trường hợp này |

**Mẹo debug nhanh:** thêm `print(...)` ngay trong hàm, hoặc dùng f-string debug `print(f"{bien=}")` (đã học ở Module 01) để in cả tên biến lẫn giá trị. Nhớ xóa `print` khi xong.

---

## 5. Khi bị kẹt: thang gợi ý 4 nấc

Hãy cho phép mình kẹt **15–20 phút** cho mỗi hàm. Đó là thời gian não đang học. Quá thời gian đó thì leo lần lượt từng nấc, **chỉ leo nấc tiếp theo khi nấc hiện tại không giúp được**:

1. **Đọc lại docstring và các dòng `assert`** của hàm đó. Viết ra giấy: input là gì, output mong đợi là gì, làm bằng tay một ví dụ.
2. **Quay lại mục README tương ứng** (xem cột "Mục README liên quan" ở [mục 6](#6-hướng-dẫn-riêng-cho-từng-module)) và thử lại ví dụ trong REPL.
3. **Giải bài toán nhỏ hơn trong REPL**. Ví dụ với `sliding_windows`, trước tiên chỉ in ra các chỉ số bắt đầu `i` hợp lệ, sau đó mới tạo slice.
4. **Mở `solutions.py`, chỉ xem ĐÚNG hàm đang kẹt**, đọc hiểu, rồi **đóng file lại** và tự gõ lời giải theo trí nhớ. Đánh dấu hàm đó để làm lại vào hôm sau (dùng `exercises_blank.py`).

---

## 6. Hướng dẫn riêng cho từng module

### Module 01: Core Syntax, Mutability & Slicing

| Bài tập | Mục README liên quan | Điểm cần chú ý |
| :--- | :--- | :--- |
| `split_train_val_test` | §6 Slicing | Tính chỉ số cắt bằng `int(n * ratio)`. Phần `test` là **phần còn lại**, không tính bằng ratio |
| `normalize_matrix_safe` | §4 Mutability & Copy | **Không được sửa** `matrix` đầu vào; trả về list mới. Xử lý trường hợp max = 0 |
| `sliding_windows` | §6 Slicing | Có bao nhiêu cửa sổ? (`len - size + 1`). Xử lý `window_size <= 0` |
| `format_training_log` | §5 F-strings | `{epoch:02d}`, `{x:.4f}`; kiểm tra `None` bằng `is not None`, không dùng `if val_acc:` (vì `0.0` là falsy!) |
| `early_stopping_epoch` | §7 `break`/`continue` | Loss **bằng** best không tính là cải thiện; dừng **ngay** khi `wait == patience` |
| `parse_command` | §8 `match-case` | Dùng guard `if n.isdigit()` cho `train`; `case _:` cho mọi trường hợp còn lại |

**Phải giải thích được:** `==` và `is`; vì sao `[[0]*3]*3` sai; shallow copy và deep copy; `-7 // 2 == -4`; slicing vượt biên không lỗi còn indexing thì lỗi; khi nào khối `for...else` chạy; vì sao `round(2.5) == 2`; `x += [4]` khác `x = x + [4]` thế nào; `break` và `continue`; vì sao `case x:` luôn khớp.

### Module 02: Data Structures & Comprehensions

| Bài tập | Mục README liên quan | Điểm cần chú ý |
| :--- | :--- | :--- |
| `build_vocab` | §4 dict, §8 `Counter` | `<pad>`=0, `<unk>`=1 luôn có; các từ còn lại **sắp xếp a→z**, id bắt đầu từ 2 |
| `encode_sentence` | §4 `dict.get` | Từ lạ thì dùng `vocab["<unk>"]`. Nhớ `.lower()` giống như lúc build |
| `batch_generator` | §7 `yield` | Dùng `yield`, không `return` list. Batch cuối có thể ngắn hơn. `batch_size <= 0` thì `raise ValueError` |
| `compute_accuracy` | §6 `zip` | List rỗng thì trả về `0.0` (tránh chia cho 0) |
| `top_k_documents` | §10 `heapq` | `heapq.nlargest(k, scores.items(), key=...)`; `k <= 0` thì trả về `[]` |
| `take_valid` | §9 iterator, §10 `islice` | Test dùng stream **vô hạn**: gọi `list(stream)` là treo máy. Hãy dùng generator + `islice` |
| `rank_words` | §8 `Counter`, §10 key tuple | `key=lambda w: (-counts[w], w)`: dấu `-` để tần suất giảm dần |

**Phải giải thích được:** `append` và `extend`; `.sort()` và `sorted()`; `(42)` và `(42,)`; `{}` là dict chứ không phải set; vì sao generator chỉ duyệt được 1 lần; iterable khác iterator thế nào; `for` hoạt động bên dưới ra sao (`iter`/`next`/`StopIteration`); sort ổn định là gì; khi nào dùng `heapq` thay vì `sorted`.

### Module 03: Functions, Type Hints & Decorators

| Bài tập | Mục README liên quan | Điểm cần chú ý |
| :--- | :--- | :--- |
| `append_metric` | §1 Mutable Default Argument | Mặc định là `None`, tạo list mới **bên trong** hàm |
| `compose_transforms` | §1 `*args`, §5 hàm trả về hàm | Trả về **một hàm**, không phải kết quả. Áp dụng `f1` trước rồi mới đến `f2`… |
| `merge_configs` | §1 `**kwargs` | Không sửa `base`: `{**base, **overrides}` hoặc `base \| overrides` |
| `count_calls` | §5 Decorator | `@wraps(func)`; bộ đếm lưu ở `wrapper.calls` |
| `make_scalers` | §3 Closure Late Binding | `lambda x, f=f: x * f` để "chốt" giá trị tại mỗi vòng |
| `make_running_mean` | §2 Closure & `nonlocal` | Lưu `total`, `count` ở hàm cha; `nonlocal` vì có phép gán `+=` |
| `flatten_config` | §6 Đệ quy | Base case: value không phải dict. Recursive case: gọi lại với `parent_key` mới |

**Phải giải thích được:** vì sao `def f(x, lst=[])` nguy hiểm; quy tắc LEGB; closure late binding trong vòng lặp `lambda`; decorator thực chất là `f = deco(f)`; khi nào cần `nonlocal`; base case trong đệ quy; nguyên nhân của `RecursionError`.

### Module 04: OOP cho AI

| Bài tập | Mục README liên quan | Điểm cần chú ý |
| :--- | :--- | :--- |
| `TrainConfig` | §5 `@dataclass` | Chỉ cần khai báo 3 trường kèm kiểu và giá trị mặc định |
| `MiniDataset` | §4 Dunder methods | `__len__`, `__getitem__`; `raise ValueError` khi số feature khác số label; nếu có `transform` thì áp dụng |
| `Linear1D`, `ReLU` | §3 Kế thừa, §4 `nn.Module` | Chỉ viết `forward`; `__call__` đã có sẵn ở `BaseModule` |
| `Sequential` | §4 | Lưu `layers`, rồi cho `x` lần lượt đi qua từng layer: `x = layer(x)` |
| `TrackedModel` | §1 Class attribute | Tăng `TrackedModel.instance_count`, **không** tăng `self.instance_count`; `self.layers = []` trong `__init__` |
| `StepLRScheduler` | §2 `@property` | `lr` là property **không có setter**, tính lại từ `epoch` mỗi lần đọc |
| `MiniDataLoader` | §6 `__iter__` | `__iter__` dùng `yield` để duyệt lại được; `len` = làm tròn lên (`math.ceil`) |

**Phải giải thích được:** class attribute và instance attribute (gán `m1.x = ...` khác với mutate list của class); `@staticmethod`, `@classmethod` và `@property`; vì sao PyTorch gọi `model(x)` mà không gọi `model.forward(x)`; `ABC`/`@abstractmethod` khác `raise NotImplementedError` ở điểm nào; 2 cách làm class duyệt được bằng `for`.

### Module 05: File I/O, JSONL & Exceptions

| Bài tập | Mục README liên quan | Điểm cần chú ý |
| :--- | :--- | :--- |
| `load_valid_jsonl` | §2 đọc từng dòng, §3 JSONL, §4 `try/except` | Bỏ qua dòng trống; bắt **đúng** `json.JSONDecodeError` (đừng `except:` trần); `"text"` rỗng sau `.strip()` thì bỏ |
| `save_json_summary` | §1 `pathlib`, §3 JSON | `mkdir(parents=True, exist_ok=True)`; ghi bằng `encoding="utf-8"` |
| `safe_to_float` | §4 `try/except/else/finally` | Test kiểm tra **thứ tự** ghi log, nên phải dùng đúng cả 4 khối |
| `temporary_setting` | §2 `@contextmanager` | `try: yield` / `finally: khôi phục`; phân biệt "chưa có key" với "key có giá trị `None`" |
| `Timer` | §2 `__enter__`/`__exit__` | `__enter__` trả về `self`; `__exit__` trả về `False` để không nuốt lỗi |

> Test sẽ tạo file `tmp_summary.json` rồi tự xóa. Nếu test fail giữa chừng, file này có thể còn sót lại; cứ xóa đi, không sao.

**Phải giải thích được:** thứ tự chạy của `try / except / else / finally` (và chuyện `return` trong `finally` ghi đè giá trị trả về); vì sao nên đọc file lớn từng dòng; `if __name__ == "__main__":` dùng để làm gì; tác dụng của môi trường ảo; thứ tự các khối `except`; `with` gọi những method nào và khi nào.

### Module 06: Vectorization & Toán AI

| Bài tập | Mục README liên quan | Điểm cần chú ý |
| :--- | :--- | :--- |
| `dot_product` | §3 | `sum(x * y for x, y in zip(a, b))`; độ dài khác nhau thì `ValueError` (vì `zip` sẽ **âm thầm** cắt ngắn!) |
| `cosine_similarity` | §3 | Tái sử dụng `dot_product`; norm = 0 thì trả về `0.0` |
| `softmax` | §3 | **Trừ `max(logits)`** trước khi `math.exp`, nếu không sẽ tràn số; tổng kết quả phải bằng 1 |
| `matmul` | §2 Shape, §3 | Kiểm tra shape `(m×k)·(k×n)`; mẹo: `zip(*B)` để lấy các cột của B |

**Phải giải thích được:** vì sao vòng lặp Python chậm so với NumPy; shape, axis và broadcasting; ý nghĩa của cosine similarity trong tìm kiếm ngữ nghĩa.

### Module 07: Text: Regex, Unicode & Random

| Bài tập | Mục README liên quan | Điểm cần chú ý |
| :--- | :--- | :--- |
| `clean_text` | §1.3 `re.sub`, §2.2 NFC | Làm **đúng thứ tự**: NFC, lower, thay URL, gộp khoảng trắng |
| `tokenize_vi` | §1.7, §2.2 | `\w+` thay vì `[a-z]+`; chuẩn hóa NFC **trước** |
| `remove_accents` | §2.3 | NFD rồi lọc `combining`; `đ`/`Đ` phải thay thủ công |
| `parse_log_line` | §1.4, §1.5 named group | Dùng `search` (không phải `match`) vì có chữ đứng trước; ép kiểu `int`/`float`; không khớp thì trả về `None` |
| `shuffle_split` | §3.2 seed | `.copy()` trước khi shuffle; `random.Random(seed)`; nhớ `shuffle` trả về `None` |

**Phải giải thích được:** vì sao luôn dùng `r"..."`; `match`, `search` và `fullmatch` khác nhau thế nào; `findall` trả về gì khi có group; greedy và non-greedy; `str` và `bytes`; vì sao `"việt" == "việt"` có thể là `False`; vì sao phải đặt seed.

---

## 7. Capstone: cách học một project có sẵn code

⚠️ **Khác với các module:** `capstone_mini_rag_search/main.py` **đã được viết hoàn chỉnh**, không có `# TODO`. Nhiệm vụ của bạn là **đọc hiểu**, rồi **mở rộng**.

**Bước 1. Chạy thử**
```bash
python3 capstone_mini_rag_search/main.py           # demo tìm kiếm
python3 capstone_mini_rag_search/test_pipeline.py  # phải in ra "...PASS!"
```

**Bước 2. Đọc code theo đúng thứ tự dữ liệu chảy qua**, kèm module đã học tương ứng:

| Thứ tự | Thành phần trong `main.py` | Kiến thức dùng |
| :--- | :--- | :--- |
| 1 | `load_corpus` đọc `corpus.jsonl` | Module 05 |
| 2 | `Document` (`@dataclass`) | Module 04 |
| 3 | `tokenize` (regex, `.lower()`) | Module 07 (regex), Module 01 |
| 4 | `TextVectorizer.fit` / `transform` (vocab, `Counter`) | Module 02 |
| 5 | `cosine_similarity` | Module 06 |
| 6 | `MiniSearchEngine.search` (`sorted(key=...)`, top-k) | Module 03 |

**Bước 3. Lần theo một truy vấn bằng tay.** Trong REPL:
```bash
cd capstone_mini_rag_search && python3
```
```python
>>> from main import *
>>> from pathlib import Path
>>> docs = load_corpus(Path("corpus.jsonl"))
>>> tokenize("Tensors and Neural Networks!")   # in từng bước trung gian
>>> engine = MiniSearchEngine(docs)
>>> engine.search("tensors and neural networks", top_k=3)
```
Tự trả lời: vector của câu truy vấn trông như thế nào? Vì sao `doc1` có điểm cao nhất?

**Bước 4. Kiểm tra hiểu bằng cách tự viết lại.** Mở một file trống và viết lại `TextVectorizer` cùng `search` mà không nhìn code gốc. Chạy test để kiểm chứng.

**Bước 5. Thử thách mở rộng** (sau mỗi thay đổi, chạy lại `test_pipeline.py` để chắc mình không làm hỏng gì):
- [ ] Loại bỏ stopwords (`"is"`, `"the"`, `"a"`, `"for"`…) trong `tokenize()`.
- [ ] Nâng cấp từ TF lên **TF-IDF** để từ hiếm có trọng số cao hơn.
- [ ] Thay `tokenize()` bằng `tokenize_vi()` (Module 07), thêm vài tài liệu tiếng Việt vào `corpus.jsonl`, rồi thử tìm kiếm bằng tiếng Việt. (Lưu ý: test kiểm tra `len(docs) == 5`, nên hãy tạo một file corpus riêng để thử.)
- [ ] Trong `search()`, thay `scored.sort(...)` + `scored[:top_k]` bằng `heapq.nlargest` (Module 02).

---

## 8. Bài test thử (Mock Test)

```bash
python3 mock_entry_test.py
```

Bài test có 20 câu trắc nghiệm. Gõ `A`/`B`/`C`/`D` rồi Enter; sau mỗi câu sẽ có đáp án và giải thích. Nhấn `Ctrl+C` nếu muốn thoát giữa chừng. Cuối bài, chương trình **tự liệt kê các phần cần ôn lại** cho từng câu bạn làm sai.

**Nên làm 2 lần:**
1. **Trước khi học Module 01**: để biết mình đang quên những gì. Đừng buồn nếu điểm thấp, vì có những câu về kiến thức bạn chưa học tới.
2. **Sau khi xong Module 07**: mục tiêu là **≥ 16/20 (80%)**.

**Sai câu nào thì ôn module nào:**

| Câu | Chủ đề | Ôn lại |
| :--- | :--- | :--- |
| 1 | Bẫy ma trận `[[0]*2]*2` | Module 01, §4 |
| 2 | Mutable default argument | Module 03, §1 |
| 3 | `==` và `is` | Module 01, §2 |
| 4 | Tuple 1 phần tử `(42,)` | Module 02, §3 |
| 5 | Closure late binding | Module 03, §3 |
| 6 | Generator chỉ duyệt 1 lần | Module 02, §7 |
| 7 | Indexing và slicing vượt biên | Module 01, §6 |
| 8 | Class attribute và instance attribute | Module 04, §1 |
| 9 | `return` trong `finally` | Module 05, §4 |
| 10 | Sắp xếp dict theo value | Module 03, §3 |
| 11 | `round(2.5)` | Module 01, §1 |
| 12 | `+=` với list | Module 01, §4 |
| 13 | Iterator và `next()` | Module 02, §9 |
| 14 | Sort ổn định với `key=len` | Module 02, §10 |
| 15 | Thiếu `nonlocal` | Module 03, §2 |
| 16 | `case x:` luôn khớp | Module 01, §8 |
| 17 | `@property` không có setter | Module 04, §2 |
| 18 | Thứ tự các khối `except` | Module 05, §4 |
| 19 | `re.match` và `re.search` | Module 07, §1.4 |
| 20 | `random.shuffle` trả về `None` | Module 07, §3.1 |

---

## 9. Lịch học gợi ý

**Lịch 3 tuần (khoảng 1.5 giờ/ngày, nghỉ chủ nhật):**

| Ngày | Việc cần làm |
| :--- | :--- |
| 1 | Chuẩn bị (mục 0), Mock Test lần 1, đọc README Module 01 (§1–§6) |
| 2 | Module 01: đọc §7–§8 + làm bài tập + so sánh lời giải |
| 3 | Module 02: README |
| 4 | Module 02: bài tập · **Làm lại** Module 01 từ `exercises_blank.py` (≈20 phút) |
| 5 | Module 03: README |
| 6 | Module 03: bài tập · Làm lại Module 02 |
| 7 | Nghỉ / ôn lại `notes.md` |
| 8 | Module 04: README |
| 9 | Module 04: bài tập · Làm lại Module 03 |
| 10 | Module 05: README + bài tập |
| 11 | Module 06: README + bài tập · Làm lại Module 04 |
| 12 | Module 07: README (§1 Regex) |
| 13 | Module 07: README (§2–§3) + bài tập |
| 14 | Nghỉ / ôn lại `notes.md` |
| 15 | Capstone: chạy, đọc, lần theo truy vấn (bước 1–3) |
| 16 | Capstone: tự viết lại (bước 4) |
| 17 | Capstone: thử thách mở rộng (bước 5) |
| 18 | Mock Test lần 2, rồi ôn các câu sai theo bảng ở mục 8 |
| 19–20 | Làm lại Module 05–07 từ bản trống, đọc lại `notes.md` |

**Học dồn cuối tuần (khoảng 4 giờ/buổi):** mỗi buổi khoảng 1.5 module, tổng cộng khoảng 7 buổi, trong đó buổi cuối dành cho Capstone và Mock Test. Nên xen một buổi "làm lại từ bản trống" giữa các buổi.

---

## 10. Bảng theo dõi tiến độ

Sửa `[ ]` thành `[x]` khi hoàn thành:

| Module | Đọc README | Test PASS | So sánh lời giải | Làm lại lần 2 |
| :--- | :---: | :---: | :---: | :---: |
| 01 | [ ] | [ ] | [ ] | [ ] |
| 02 | [ ] | [ ] | [ ] | [ ] |
| 03 | [ ] | [ ] | [ ] | [ ] |
| 04 | [ ] | [ ] | [ ] | [ ] |
| 05 | [ ] | [ ] | [ ] | [ ] |
| 06 | [ ] | [ ] | [ ] | [ ] |
| 07 | [ ] | [ ] | [ ] | [ ] |
| Capstone | [ ] chạy & đọc | [ ] tự viết lại | [ ] stopwords / TF-IDF | [ ] tiếng Việt / heapq |
| Mock Test | Lần 1: ___/20 | Lần 2: ___/20 | | |

**Cách kiểm tra nhanh toàn bộ bài tập:**
```bash
for d in 0*/; do python3 "$d/exercises.py" 2>&1 | tail -1; done
```
Module nào in ra `PASS` là đã xong; module nào in ra tên lỗi là còn phải làm.

---

## 11. Bước tiếp theo sau khóa học

Khi đã tick hết bảng tiến độ và đạt Mock Test ≥ 16/20, bạn sẵn sàng sang hệ sinh thái AI thực chiến:

1. **NumPy**: thay vòng lặp bằng tính toán ma trận/vector (Module 06 là bước đệm trực tiếp).
2. **Pandas & Matplotlib/Seaborn**: phân tích, làm sạch và trực quan hóa dữ liệu (EDA).
3. **Scikit-learn**: các thuật toán ML cổ điển (Regression, Tree, Clustering, Evaluation metrics).
4. **PyTorch**: mạng neural, Autograd, training loop (lúc này bạn sẽ thấy Module 04 cực kỳ hữu ích).
5. **HuggingFace / LLM APIs**: fine-tuning, RAG, xây dựng ứng dụng AI (Capstone chính là bản thu nhỏ của phần Retrieval trong RAG).

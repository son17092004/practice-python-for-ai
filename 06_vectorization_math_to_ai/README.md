# Module 06: Tư duy Vectorization & Toán học AI (Chi tiết)

Module này là cầu nối trực tiếp từ **Python thuần** sang **NumPy & PyTorch**. Bạn sẽ hiểu *tại sao* AI cần thư viện chuyên dụng và *bên dưới* các hàm AI hoạt động như thế nào.

---

## 1. Tại sao `list` Python thuần chậm trong AI?

1. **Boxing & Con trỏ phân tán**: Một `list` Python thực chất chứa các con trỏ trỏ tới từng `PyObject` nằm rải rác trong RAM (mỗi `float` tốn ~24 bytes + chi phí con trỏ). Trong khi đó, `numpy.ndarray` hay `torch.Tensor` lưu toàn bộ số liên tiếp trong một khối RAM phẳng, CPU/GPU có thể nạp vào thanh ghi SIMD xử lý hàng loạt.
2. **Dynamic Dispatch**: Trong vòng lặp `for`, ở mỗi bước Python đều phải kiểm tra kiểu của `a[i]` và `b[i]` rồi mới tìm hàm `+` tương ứng.
3. **GIL (Global Interpreter Lock)**: Một tiến trình Python chuẩn chỉ chạy bytecode trên 1 luồng CPU tại một thời điểm (trừ các thư viện C/C++/CUDA như NumPy, PyTorch có thể giải phóng GIL).

---

## 2. Khái niệm Shape, Axis & Broadcasting (Chuẩn bị cho NumPy/PyTorch)

- **Shape (Kích thước)**:
  - Vector (1D): `[1, 2, 3]` → shape `(3,)`
  - Ma trận (2D): `[[1, 2, 3], [4, 5, 6]]` → shape `(2, 3)` (2 dòng, 3 cột)
  - Batch ảnh (4D trong Deep Learning): `(B, C, H, W)` (Batch size, Channels, Height, Width)
- **Axis (Trục)**:
  - `axis=0`: Tính dọc theo các **dòng** (gộp từng cột lại).
  - `axis=1`: Tính ngang theo các **cột** (gộp từng dòng lại).
- **Broadcasting**: Tự động mở rộng mảng nhỏ để tính toán với mảng lớn hơn mà không cần viết vòng lặp (ví dụ: trừ đi giá trị trung bình của mỗi cột cho toàn bộ ma trận).

---

## 3. Bốn phép toán xương sống của AI

1. **Dot Product (Tích vô hướng)**:
   $$\mathbf{a} \cdot \mathbf{b} = \sum_{i=1}^{n} a_i b_i$$
   - Ý nghĩa hình học: Đo độ cùng hướng giữa 2 vector. Là phép toán cốt lõi trong lớp `Linear` ($y = Wx + b$) và cơ chế **Self-Attention** ($QK^T$) của Transformer/LLM.

2. **L2 Norm & Cosine Similarity**:
   $$\text{cosine}(\mathbf{a}, \mathbf{b}) = \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|_2 \|\mathbf{b}\|_2}, \quad \|\mathbf{a}\|_2 = \sqrt{\sum_i a_i^2}$$
   - Giá trị nằm trong $[-1, 1]$ ($1$: giống hệt hướng, $0$: vuông góc/không liên quan, $-1$: ngược hướng). Dùng làm thước đo tìm kiếm văn bản trong **RAG / Vector Database**.

3. **Softmax & Ổn định số học (Numerical Stability)**:
   $$\text{softmax}(x_i) = \frac{e^{x_i - \max(x)}}{\sum_j e^{x_j - \max(x)}}$$
   - Biến vector logits bất kỳ thành xác suất (mỗi phần tử $\in (0, 1)$, tổng $= 1$).
   - **Tại sao phải trừ $\max(x)$?** Vì $e^{1000}$ trong Python/float64 sẽ gây `OverflowError` (hoặc `inf / inf = NaN`). Trừ đi $\max(x)$ giữ cho số mũ luôn $\le 0$, nên $e^{x_i - \max(x)} \in (0, 1]$ mà **kết quả toán học không hề thay đổi**!

4. **Matrix Multiplication (Nhân ma trận)**:
   - Ma trận $A$ kích thước $(m \times k)$ nhân với $B$ kích thước $(k \times n)$ cho ra $C$ kích thước $(m \times n)$.
   - Điều kiện bắt buộc: **Số cột của $A$ phải bằng số dòng của $B$** ($k = k$).

---

## 4. Bảng ánh xạ: Python thuần → NumPy → PyTorch

Khi học xong module này và chuyển sang NumPy/PyTorch, bạn sẽ thấy mọi thứ quen thuộc ngay lập tức:

| Phép toán | Python thuần | NumPy | PyTorch |
| :--- | :--- | :--- | :--- |
| Tích vô hướng | `sum(x*y for x,y in zip(a,b))` | `np.dot(a, b)` | `torch.dot(a, b)` |
| Nhân ma trận | `matmul(A, B)` | `A @ B` | `A @ B` |
| Chuẩn L2 | `math.sqrt(sum(x*x for x in a))` | `np.linalg.norm(a)` | `torch.norm(a)` |
| Softmax | `exps / sum(exps)` | `scipy.special.softmax(x)` | `torch.softmax(x, dim=-1)` |

---

## Thực hành

Mở [exercises.py](./exercises.py) và chạy kiểm tra:
```bash
python3 06_vectorization_math_to_ai/exercises.py
```

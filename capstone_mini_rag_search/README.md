# Capstone Mini-Project: Mini Search Engine (Nền tảng của RAG)

Dự án nhỏ này kết hợp **toàn bộ kiến thức từ Module 01 đến Module 06** để xây dựng một bộ máy tìm kiếm văn bản (Information Retrieval — bước đầu tiên trong hệ thống **RAG - Retrieval-Augmented Generation**) hoàn toàn bằng Python thuần.

## Kiến trúc Pipeline

1. **Đọc dữ liệu (`corpus.jsonl`)**: Dùng `pathlib.Path` + `json` (Module 05).
2. **Đóng gói dữ liệu (`Document`)**: Dùng `@dataclass` (Module 04).
3. **Tokenize & Vector hóa (`TextVectorizer`)**: Xây vocab từ corpus (`Counter`, `dict`), chuyển câu văn thành vector TF (Term Frequency) (Module 02).
4. **Tìm kiếm (`MiniSearchEngine`)**: Tính `cosine_similarity` giữa câu truy vấn và từng tài liệu, sắp xếp và trả về `top_k` kết quả tốt nhất (Module 01, 03, 06).

## Chạy thử

```bash
# Chạy demo tìm kiếm
python3 capstone_mini_rag_search/main.py

# Chạy bộ test kiểm tra toàn bộ pipeline
python3 capstone_mini_rag_search/test_pipeline.py
```

## Thử thách mở rộng cho bạn
- Thêm bước loại bỏ stopwords (`"is"`, `"the"`, `"a"`, `"for"`...) vào `tokenize()`.
- Nâng cấp từ TF (Term Frequency) lên **TF-IDF** để các từ hiếm mang nhiều trọng số hơn!

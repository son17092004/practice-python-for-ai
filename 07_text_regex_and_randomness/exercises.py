"""Module 07: Bài tập Regex, Unicode & Randomness."""

import random
import re
import unicodedata


def clean_text(text: str) -> str:
    """Làm sạch một câu văn bản theo đúng thứ tự:

    1. Chuẩn hóa Unicode về NFC.
    2. Chuyển về chữ thường.
    3. Thay mọi URL bắt đầu bằng "http://" hoặc "https://" (kéo dài đến khoảng trắng kế tiếp)
       bằng token "<url>".
    4. Gộp mọi chuỗi khoảng trắng liên tiếp (space, tab, xuống dòng) thành 1 dấu cách,
       và bỏ khoảng trắng ở 2 đầu.

    Ví dụ: "  Xem   https://abc.com/x?y=1  NGAY\\n bây giờ " -> "xem <url> ngay bây giờ"
    """
    # TODO: Viết code tại đây
    pass


def tokenize_vi(text: str) -> list[str]:
    """Tách từ hỗ trợ tiếng Việt (sửa lỗi của `tokenize()` trong Capstone):

    - Chuẩn hóa NFC, chuyển chữ thường, rồi lấy mọi chuỗi ký tự "chữ" bằng regex `\\w+`.
    Ví dụ: "Học máy, 2024!" -> ["học", "máy", "2024"]
    Văn bản dạng NFD phải cho ra CÙNG kết quả với dạng NFC.
    """
    # TODO: Viết code tại đây
    pass


def remove_accents(text: str) -> str:
    """Bỏ dấu tiếng Việt: "Tiếng Việt Đẹp" -> "Tieng Viet Dep".

    Gợi ý: NFD + lọc `unicodedata.combining(c)`; xử lý riêng "đ"/"Đ".
    """
    # TODO: Viết code tại đây
    pass


def parse_log_line(line: str) -> dict | None:
    """Trích xuất metric từ một dòng log training bằng regex có NAMED GROUP.

    Dòng hợp lệ chứa (theo đúng thứ tự, cách nhau bởi khoảng trắng):
        epoch=<số nguyên> loss=<số thực> acc=<số thực>
    Có thể có chữ khác ở trước/sau (ví dụ "[INFO] ...").

    Trả về {"epoch": int, "loss": float, "acc": float}, hoặc None nếu dòng không khớp.
    Ví dụ: "[INFO] epoch=3 loss=0.1234 acc=0.91" -> {"epoch": 3, "loss": 0.1234, "acc": 0.91}
    """
    # TODO: Viết code tại đây
    pass


def shuffle_split(data: list, train_ratio: float, seed: int) -> tuple[list, list]:
    """Xáo trộn rồi chia `data` thành (train, test).

    - KHÔNG được thay đổi `data` gốc.
    - Dùng `random.Random(seed)` (không dùng `random.seed` toàn cục).
    - Cùng `seed` thì phải cho ra cùng kết quả.
    - len(train) = int(len(data) * train_ratio), test là phần còn lại.
    """
    # TODO: Viết code tại đây
    pass


if __name__ == "__main__":
    # Test 1: clean_text
    assert clean_text("  Xem   https://abc.com/x?y=1  NGAY\n bây giờ ") == "xem <url> ngay bây giờ"
    assert clean_text("Link: http://a.vn và https://b.io/p") == "link: <url> và <url>"
    assert clean_text(unicodedata.normalize("NFD", "Việt")) == "việt", "Quên chuẩn hóa NFC?"

    # Test 2: tokenize_vi
    assert tokenize_vi("Học máy, 2024!") == ["học", "máy", "2024"]
    nfd_text = unicodedata.normalize("NFD", "Tiếng Việt")
    assert tokenize_vi(nfd_text) == ["tiếng", "việt"], "Văn bản NFD phải được chuẩn hóa về NFC!"

    # Test 3: remove_accents
    assert remove_accents("Tiếng Việt Đẹp") == "Tieng Viet Dep"
    assert remove_accents("đường hầm") == "duong ham"
    assert remove_accents("no accents") == "no accents"

    # Test 4: parse_log_line
    assert parse_log_line("[INFO] epoch=3 loss=0.1234 acc=0.91") == {
        "epoch": 3,
        "loss": 0.1234,
        "acc": 0.91,
    }
    assert parse_log_line("epoch=12 loss=1.5 acc=0.5 lr=0.001") == {
        "epoch": 12,
        "loss": 1.5,
        "acc": 0.5,
    }
    assert parse_log_line("training started") is None
    assert parse_log_line("epoch=x loss=0.1 acc=0.2") is None

    # Test 5: shuffle_split
    original = list(range(20))
    tr1, te1 = shuffle_split(original, 0.8, seed=42)
    tr2, te2 = shuffle_split(original, 0.8, seed=42)
    tr3, _ = shuffle_split(original, 0.8, seed=7)
    assert original == list(range(20)), "Không được xáo trộn dữ liệu gốc!"
    assert len(tr1) == 16 and len(te1) == 4
    assert sorted(tr1 + te1) == original, "Không được mất hay trùng phần tử!"
    assert (tr1, te1) == (tr2, te2), "Cùng seed phải cho cùng kết quả!"
    assert tr1 != tr3, "Khác seed nên cho kết quả khác"
    assert tr1 != original[:16], "Dữ liệu chưa được xáo trộn!"

    print("Module 07: Tất cả bài test đã PASS!")

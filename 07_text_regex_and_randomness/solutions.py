"""Module 07: Lời giải tham khảo."""

import random
import re
import unicodedata

URL_RE = re.compile(r"https?://\S+")
WS_RE = re.compile(r"\s+")
LOG_RE = re.compile(
    r"epoch=(?P<epoch>\d+)\s+loss=(?P<loss>\d+(?:\.\d+)?)\s+acc=(?P<acc>\d+(?:\.\d+)?)"
)


def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text).lower()
    text = URL_RE.sub("<url>", text)
    return WS_RE.sub(" ", text).strip()


def tokenize_vi(text: str) -> list[str]:
    return re.findall(r"\w+", unicodedata.normalize("NFC", text).lower())


def remove_accents(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text)
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    return stripped.replace("đ", "d").replace("Đ", "D")


def parse_log_line(line: str) -> dict | None:
    if (m := LOG_RE.search(line)) is None:
        return None
    return {
        "epoch": int(m["epoch"]),
        "loss": float(m["loss"]),
        "acc": float(m["acc"]),
    }


def shuffle_split(data: list, train_ratio: float, seed: int) -> tuple[list, list]:
    shuffled = data.copy()
    random.Random(seed).shuffle(shuffled)
    cut = int(len(shuffled) * train_ratio)
    return shuffled[:cut], shuffled[cut:]


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

    print("Module 07 (solutions): Tất cả bài test đã PASS!")

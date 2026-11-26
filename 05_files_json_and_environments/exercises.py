"""Module 05: Bài tập File I/O, JSONL & Exceptions."""

import json
import time
from contextlib import contextmanager
from pathlib import Path


def load_valid_jsonl(path: Path) -> tuple[list[dict], int]:
    """Đọc file JSONL tại `path`, trả về `(valid_records, error_count)`.

    Quy tắc:
    1. Bỏ qua các dòng trống (chỉ chứa khoảng trắng).
    2. Nếu dòng bị lỗi `json.JSONDecodeError`, tăng `error_count` lên 1 và bỏ qua dòng đó.
    3. Chỉ giữ các record hợp lệ có trường `"text"` không rỗng sau khi `.strip()`.
    """
    # TODO: Viết code tại đây
    valid_records: list[dict] = []
    error_count = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                text = record.get("text")
                if isinstance(text, str) and text.strip():
                    valid_records.append(record)
            except json.JSONDecodeError:
                error_count+=1
    return valid_records,error_count


 

def save_json_summary(records: list[dict], out_path: Path) -> None:
    """Lưu thống kê số lượng từng `label` ra file JSON tại `out_path`.

    Ví dụ output JSON: {"total": 3, "label_counts": {"positive": 2, "negative": 1}}
    Gợi ý: Đảm bảo thư mục cha tồn tại bằng `out_path.parent.mkdir(parents=True, exist_ok=True)`.
    """
    # TODO: Viết code tại đây
    label_counts: dict = dict()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, mode='w', encoding="utf-8") as f:
        for rc in records:
            lbl = rc["label"]
            label_counts[lbl] = label_counts.get(lbl, 0) + 1
        result: dict = {
            "total": len(records),
            "label_counts": label_counts
        }
        json.dump(result, f, ensure_ascii=True, indent=2)

def safe_to_float(text: str, log: list[str]) -> float | None:
    """Chuyển `text` thành float, ghi lại các bước vào `log` bằng ĐỦ 4 khối try/except/else/finally:

    - try:     chỉ chứa phép chuyển đổi `float(text)`.
    - except ValueError: thêm "error:<text>" vào log, kết quả là None.
    - else:    thêm "ok:<text>" vào log.
    - finally: LUÔN thêm "done" vào log.

    Ví dụ: safe_to_float("1.5", log) -> 1.5, log == ["ok:1.5", "done"]
           safe_to_float("abc", log) -> None, log == ["error:abc", "done"]
    """
    # TODO: Viết code tại đây
    result = None
    try:
        result = float(text)
    except ValueError as e:
        log.append(f"error:{text}")
    else:
        log.append(f"ok:{text}")
    finally:
        log.append("done")
    return result

@contextmanager
def temporary_setting(config: dict, key: str, value):
    """Context manager tạm thời đặt `config[key] = value` trong khối `with`.

    Khi ra khỏi khối (KỂ CẢ KHI CÓ LỖI), khôi phục trạng thái cũ:
    - Nếu `key` đã có trước đó -> trả lại giá trị cũ.
    - Nếu `key` chưa có trước đó -> xóa `key` khỏi config.
    Gợi ý: try / finally quanh `yield`.
    """
    # TODO: Viết code tại đây
    value_before = config.get(key)
    config[key] = value
    try:
        yield
    finally:
        if not value_before:
            config.pop(key)
        else:
            config[key] = value_before


class Timer:
    """Context manager dạng class đo thời gian chạy khối `with`.

    - __enter__: ghi thời điểm bắt đầu (`time.perf_counter()`), trả về `self`.
    - __exit__: lưu `self.elapsed` (giây, float >= 0) và KHÔNG nuốt exception.
    """
    # TODO: Viết code tại đây
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    def __exit__(self, exc_type, exc, tb):
        self.elapsed = float(time.perf_counter()-self.start)
        return False


if __name__ == "__main__":
    base_dir = Path(__file__).parent
    sample_path = base_dir / "sample_data.jsonl"

    records, errors = load_valid_jsonl(sample_path)
    assert errors == 1
    assert len(records) == 3
    assert [r["id"] for r in records] == [1, 3, 4]

    out_file = base_dir / "tmp_summary.json"
    save_json_summary(records, out_file)
    summary = json.loads(out_file.read_text(encoding="utf-8"))
    assert summary == {
        "total": 3,
        "label_counts": {"positive": 2, "negative": 1},
    }
    out_file.unlink()  # Dọn dẹp file tạm sau khi test

    # Test 3: safe_to_float
    log: list[str] = []
    assert safe_to_float("1.5", log) == 1.5
    assert safe_to_float("abc", log) is None
    print(log)
    assert log == ["ok:1.5", "done", "error:abc", "done"]

    # Test 4: temporary_setting
    cfg = {"dropout": 0.1}
    with temporary_setting(cfg, "dropout", 0.0):
        assert cfg["dropout"] == 0.0
    assert cfg == {"dropout": 0.1}
    try:
        with temporary_setting(cfg, "eval_mode", True):
            assert cfg["eval_mode"] is True
            raise RuntimeError("lỗi giả lập giữa chừng")
    except RuntimeError:
        pass
    assert cfg == {"dropout": 0.1}, "Phải khôi phục config kể cả khi có lỗi!"

    # Test 5: Timer
    with Timer() as t:
        sum(range(10_000))
    assert isinstance(t.elapsed, float) and t.elapsed >= 0
    try:
        with Timer() as t2:
            raise KeyError("x")
        raise AssertionError("Timer không được nuốt exception!")
    except KeyError:
        assert t2.elapsed >= 0

    print("Module 05: Tất cả bài test đã PASS!")

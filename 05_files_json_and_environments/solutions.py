"""Module 05: Lời giải tham khảo."""

import json
import time
from collections import Counter
from contextlib import contextmanager
from pathlib import Path


def load_valid_jsonl(path: Path) -> tuple[list[dict], int]:
    valid_records: list[dict] = []
    error_count = 0

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                continue
            try:
                record = json.loads(stripped)
            except json.JSONDecodeError:
                error_count += 1
                continue

            if str(record.get("text", "")).strip():
                valid_records.append(record)

    return valid_records, error_count


def save_json_summary(records: list[dict], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    counts = dict(Counter(r.get("label", "unknown") for r in records))
    summary = {
        "total": len(records),
        "label_counts": counts,
    }
    out_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def safe_to_float(text: str, log: list[str]) -> float | None:
    result = None
    try:
        result = float(text)
    except ValueError:
        log.append(f"error:{text}")
    else:
        log.append(f"ok:{text}")
    finally:
        log.append("done")
    return result


@contextmanager
def temporary_setting(config: dict, key: str, value):
    missing = object()  # giá trị "canh gác" để phân biệt "chưa có key" với "giá trị là None"
    old = config.get(key, missing)
    config[key] = value
    try:
        yield config
    finally:
        if old is missing:
            del config[key]
        else:
            config[key] = old


class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self.start
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
    out_file.unlink()

    # Test 3: safe_to_float
    log: list[str] = []
    assert safe_to_float("1.5", log) == 1.5
    assert safe_to_float("abc", log) is None
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

    print("Module 05 (solutions): Tất cả bài test đã PASS!")

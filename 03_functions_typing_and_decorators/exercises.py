"""Module 03: Bài tập Functions, Type Hints & Decorators."""

from functools import wraps
from typing import Callable


def append_metric(
    value: float, history: list[float] | None = None
) -> list[float]:
    """Thêm `value` vào `history`. Nếu `history` là None, tạo list mới.
    Không dùng mutable default argument!
    """
    # TODO: Viết code tại đây
    if history is None:
        history = []
    history.append(value)
    return history


def compose_transforms(*funcs: Callable[[str], str]) -> Callable[[str], str]:
    """Nhận vào nhiều hàm biến đổi chuỗi f1, f2, ..., fn.
    Trả về một hàm mới thực hiện lần lượt: fn(...f2(f1(x))).

    Ví dụ: compose_transforms(str.strip, str.lower)("  HELLO ") -> "hello"
    """
    # TODO: Viết code tại đây
    def process(s: str) -> str:
        for f in funcs:
            s = f(s)
        return s
    return process

def merge_configs(base: dict, **overrides) -> dict:
    """Trả về một dict mới gộp `base` và các `overrides` (không làm thay đổi `base`)."""
    # TODO: Viết code tại đây
    return {**base, **overrides}


def count_calls(func: Callable) -> Callable:
    """Decorator đếm số lần hàm `func` được gọi, lưu vào thuộc tính `wrapper.calls`.

    Gợi ý: Dùng `@wraps(func)`, khởi tạo `wrapper.calls = 0`, tăng lên 1 mỗi lần gọi.
    """
    # TODO: Viết code tại đây
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper



def make_scalers(factors: list[float]) -> list[Callable[[float], float]]:
    """Trả về danh sách hàm, hàm thứ i nhân đầu vào với `factors[i]`.

    Ví dụ: fs = make_scalers([1, 2, 3]); [f(10) for f in fs] -> [10, 20, 30]
    CẨN THẬN bẫy Closure Late Binding (README mục 3)!
    """
    # TODO: Viết code tại đây
    return [lambda x, f=f: x*f for f in factors]


def make_running_mean() -> Callable[[float], float]:
    """Trả về một hàm `update(value)`: mỗi lần gọi sẽ ghi nhận `value` và trả về
    TRUNG BÌNH của tất cả các giá trị đã nhận tính đến lúc đó.

    Ví dụ: m = make_running_mean(); m(2) -> 2.0; m(4) -> 3.0; m(6) -> 4.0
    Yêu cầu: KHÔNG lưu cả list giá trị; chỉ lưu tổng và số lượng (dùng `nonlocal`).
    Mỗi lần gọi make_running_mean() phải tạo một bộ đếm độc lập.
    """
    # TODO: Viết code tại đây
    total = 0.0
    count = 0
    def update(value: float) -> float:
        nonlocal total, count
        total += value
        count +=1
        return total/count
    return update


def flatten_config(cfg: dict, parent_key: str = "") -> dict:
    """Làm phẳng dict lồng nhau (độ sâu bất kỳ) bằng ĐỆ QUY, nối key bằng dấu chấm.

    Ví dụ:
    {"model": {"lr": 0.1, "layers": {"n": 2}}, "seed": 1}
    -> {"model.lr": 0.1, "model.layers.n": 2, "seed": 1}
    Không được thay đổi `cfg` đầu vào.
    """
    # TODO: Viết code tại đây
    flat_cfg = {}
    for key in cfg.keys():
        if isinstance(cfg[key], dict):
            flat_cfg.update(flatten_config(cfg[key], parent_key=f"{key}" if parent_key == "" else f"{parent_key}.{key}"))
        else:
            flat_cfg[f"{parent_key}.{key}" if parent_key else key] = cfg[key]
    return flat_cfg

if __name__ == "__main__":
    # Test 1: append_metric
    h1 = append_metric(0.5)
    h2 = append_metric(0.3)
    assert h1 == [0.5]
    assert h2 == [0.3], "Lỗi mutable default argument!"

    # Test 2: compose_transforms
    clean = compose_transforms(str.strip, str.lower, lambda s: s.replace(" ", "_"))
    assert clean("  Hello AI  ") == "hello_ai"

    # Test 3: merge_configs
    base_cfg = {"lr": 1e-3, "batch_size": 32}
    new_cfg = merge_configs(base_cfg, lr=3e-4, epochs=5)
    assert new_cfg == {"lr": 3e-4, "batch_size": 32, "epochs": 5}
    assert base_cfg == {"lr": 1e-3, "batch_size": 32}

    # Test 4: count_calls
    @count_calls
    def step(x: int) -> int:
        return x + 1

    assert step(1) == 2
    assert step(2) == 3
    assert step.calls == 2
    assert step.__name__ == "step"

    # Test 5: make_scalers
    fs = make_scalers([1, 2, 3])
    assert [f(10) for f in fs] == [10, 20, 30], "Bẫy Closure Late Binding!"

    # Test 6: make_running_mean
    m1 = make_running_mean()
    m2 = make_running_mean()
    assert m1(2) == 2.0
    assert m1(4) == 3.0
    assert m2(10) == 10.0, "Hai bộ đếm phải độc lập!"
    assert m1(6) == 4.0

    # Test 7: flatten_config
    nested = {"model": {"lr": 0.1, "layers": {"n": 2}}, "seed": 1}
    assert flatten_config(nested) == {"model.lr": 0.1, "model.layers.n": 2, "seed": 1}
    assert nested == {"model": {"lr": 0.1, "layers": {"n": 2}}, "seed": 1}
    assert flatten_config({}) == {}

    print("Module 03: Tất cả bài test đã PASS!")

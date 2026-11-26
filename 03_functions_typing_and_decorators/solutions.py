"""Module 03: Lời giải tham khảo."""

from functools import wraps
from typing import Callable


def append_metric(
    value: float, history: list[float] | None = None
) -> list[float]:
    if history is None:
        history = []
    history.append(value)
    return history


def compose_transforms(*funcs: Callable[[str], str]) -> Callable[[str], str]:
    def pipeline(text: str) -> str:
        for fn in funcs:
            text = fn(text)
        return text

    return pipeline


def merge_configs(base: dict, **overrides) -> dict:
    return {**base, **overrides}


def count_calls(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


def make_scalers(factors: list[float]) -> list[Callable[[float], float]]:
    return [lambda x, f=f: x * f for f in factors]


def make_running_mean() -> Callable[[float], float]:
    total = 0.0
    count = 0

    def update(value: float) -> float:
        nonlocal total, count
        total += value
        count += 1
        return total / count

    return update


def flatten_config(cfg: dict, parent_key: str = "") -> dict:
    flat = {}
    for key, value in cfg.items():
        full_key = f"{parent_key}.{key}" if parent_key else key
        if isinstance(value, dict):
            flat.update(flatten_config(value, full_key))
        else:
            flat[full_key] = value
    return flat


if __name__ == "__main__":
    h1 = append_metric(0.5)
    h2 = append_metric(0.3)
    assert h1 == [0.5] and h2 == [0.3]

    clean = compose_transforms(str.strip, str.lower, lambda s: s.replace(" ", "_"))
    assert clean("  Hello AI  ") == "hello_ai"

    base_cfg = {"lr": 1e-3, "batch_size": 32}
    new_cfg = merge_configs(base_cfg, lr=3e-4, epochs=5)
    assert new_cfg == {"lr": 3e-4, "batch_size": 32, "epochs": 5}
    assert base_cfg == {"lr": 1e-3, "batch_size": 32}

    @count_calls
    def step(x: int) -> int:
        return x + 1

    assert step(1) == 2 and step(2) == 3
    assert step.calls == 2 and step.__name__ == "step"

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

    print("Module 03 (solutions): Tất cả bài test đã PASS!")

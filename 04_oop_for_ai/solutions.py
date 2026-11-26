"""Module 04: Lời giải tham khảo."""

import math
from dataclasses import dataclass
from typing import Callable


@dataclass
class TrainConfig:
    lr: float = 1e-3
    batch_size: int = 32
    epochs: int = 10


class MiniDataset:
    def __init__(
        self, features: list, labels: list, transform: Callable | None = None
    ):
        if len(features) != len(labels):
            raise ValueError("Số lượng features và labels phải bằng nhau")
        self.features = features
        self.labels = labels
        self.transform = transform

    def __len__(self) -> int:
        return len(self.features)

    def __getitem__(self, idx: int) -> tuple:
        x = self.features[idx]
        y = self.labels[idx]
        if self.transform is not None:
            x = self.transform(x)
        return x, y


class BaseModule:
    def __call__(self, x):
        return self.forward(x)

    def forward(self, x):
        raise NotImplementedError


class Linear1D(BaseModule):
    def __init__(self, weight: float, bias: float):
        self.weight = weight
        self.bias = bias

    def forward(self, x: list[float]) -> list[float]:
        return [self.weight * v + self.bias for v in x]


class ReLU(BaseModule):
    def forward(self, x: list[float]) -> list[float]:
        return [max(0.0, v) for v in x]


class Sequential(BaseModule):
    def __init__(self, *layers: BaseModule):
        self.layers = layers

    def forward(self, x: list[float]) -> list[float]:
        for layer in self.layers:
            x = layer(x)
        return x


class TrackedModel:
    instance_count = 0

    def __init__(self, name: str):
        self.name = name
        self.layers: list[str] = []
        TrackedModel.instance_count += 1

    def add_layer(self, layer_name: str) -> None:
        self.layers.append(layer_name)


class StepLRScheduler:
    def __init__(self, base_lr: float, gamma: float, step_size: int):
        self.base_lr = base_lr
        self.gamma = gamma
        self.step_size = step_size
        self.epoch = 0

    def step(self) -> None:
        self.epoch += 1

    @property
    def lr(self) -> float:
        return self.base_lr * self.gamma ** (self.epoch // self.step_size)


class MiniDataLoader:
    def __init__(self, dataset, batch_size: int):
        self.dataset = dataset
        self.batch_size = batch_size

    def __len__(self) -> int:
        return math.ceil(len(self.dataset) / self.batch_size)

    def __iter__(self):
        for start in range(0, len(self.dataset), self.batch_size):
            stop = min(start + self.batch_size, len(self.dataset))
            yield [self.dataset[i] for i in range(start, stop)]


if __name__ == "__main__":
    cfg = TrainConfig(epochs=5)
    assert cfg.lr == 1e-3 and cfg.batch_size == 32 and cfg.epochs == 5

    ds = MiniDataset([1, 2, 3], [10, 20, 30], transform=lambda v: v * 2)
    assert len(ds) == 3
    assert ds[1] == (4, 20)

    net = Sequential(Linear1D(weight=2.0, bias=-3.0), ReLU())
    assert net([1.0, 2.0, 3.0]) == [0.0, 1.0, 3.0]

    # Test 4: TrackedModel (class attribute vs instance attribute)
    a = TrackedModel("resnet")
    b = TrackedModel("vit")
    a.add_layer("conv")
    assert TrackedModel.instance_count == 2, "Phải tăng CLASS attribute, không phải instance!"
    assert a.layers == ["conv"] and b.layers == [], "Mỗi model phải có list layers riêng!"

    # Test 5: StepLRScheduler (@property chỉ đọc)
    sched = StepLRScheduler(base_lr=0.1, gamma=0.5, step_size=2)
    lrs = []
    for _ in range(5):
        lrs.append(sched.lr)
        sched.step()
    assert all(math.isclose(x, y) for x, y in zip(lrs, [0.1, 0.1, 0.05, 0.05, 0.025]))
    try:
        sched.lr = 1.0
        raise AssertionError("`lr` phải là thuộc tính CHỈ ĐỌC (property không có setter)!")
    except AttributeError:
        pass

    # Test 6: MiniDataLoader (iterable, duyệt lại được)
    loader = MiniDataLoader(MiniDataset([1, 2, 3, 4, 5], [0, 1, 0, 1, 0]), batch_size=2)
    assert len(loader) == 3
    epoch1 = list(loader)
    assert epoch1 == [[(1, 0), (2, 1)], [(3, 0), (4, 1)], [(5, 0)]]
    assert list(loader) == epoch1, "DataLoader phải duyệt lại được ở epoch sau!"
    assert list(MiniDataLoader([10, 20, 30], batch_size=5)) == [[10, 20, 30]]

    print("Module 04 (solutions): Tất cả bài test đã PASS!")

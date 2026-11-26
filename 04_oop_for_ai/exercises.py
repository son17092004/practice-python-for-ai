"""Module 04: Bài tập OOP cho AI."""

import math
from dataclasses import dataclass
from typing import Callable


@dataclass
class TrainConfig:
    """Cấu hình huấn luyện với giá trị mặc định:
    - lr: float = 1e-3
    - batch_size: int = 32
    - epochs: int = 10
    """
    # TODO: Khai báo các trường của dataclass tại đây
    def __init__(self, lr: float = 1e-3, batch_size: int = 32, epochs: int = 10):
        self.lr = lr
        self.batch_size = batch_size
        self.epochs = epochs
    def __repr__(self):
        pass
    def __str__(self):
        pass

class MiniDataset:
    """Mô phỏng `torch.utils.data.Dataset`.

    - __init__(self, features: list, labels: list, transform: Callable | None = None):
        Kiểm tra len(features) == len(labels), nếu không thì raise ValueError.
    - __len__(self) -> int: trả về số lượng mẫu.
    - __getitem__(self, idx: int) -> tuple:
        Lấy feature và label tại vị trí idx.
        Nếu có `transform`, áp dụng `transform(feature)` trước khi trả về `(feature, label)`.
    """
    # TODO: Viết code tại đây
    def __init__(self, features: list, labels: list, transform: Callable | None = None):
        if len(features) != len(labels):
            raise ValueError("features and labels must have the same length")
        self.features = features
        self.labels = labels
        self.transform = transform
    def __len__(self) -> int:
        return len(self.features)
    def __getitem__(self, idx: int) -> tuple:
        feature = self.features[idx]
        label = self.labels[idx]
        if self.transform:
            return (self.transform(feature), label)
        return (feature, label)
class BaseModule:
    """Lớp cha mô phỏng `torch.nn.Module`.
    Khi gọi `layer(x)` (__call__), tự động gọi `self.forward(x)`.
    """

    def __call__(self, x):
        return self.forward(x)

    def forward(self, x):
        raise NotImplementedError


class Linear1D(BaseModule):
    """Layer tuyến tính 1 chiều: y = weight * x + bias cho từng phần tử trong list `x`."""

    def __init__(self, weight: float, bias: float):
        # TODO: Lưu weight và bias
        self.weight = weight
        self.bias = bias

    def forward(self, x: list[float]) -> list[float]:
        # TODO: Trả về [self.weight * v + self.bias for v in x]
        return [self.weight * v + self.bias for v in x]


class ReLU(BaseModule):
    """Hàm kích hoạt ReLU: max(0.0, v) cho từng phần tử trong list `x`."""

    def forward(self, x: list[float]) -> list[float]:
        # TODO: Viết code tại đây
        return [max(0.0, v) for v in x]


class Sequential(BaseModule):
    """Chạy tuần tự qua danh sách các layer (mô phỏng `nn.Sequential`)."""

    def __init__(self, *layers: BaseModule):
        # TODO: Lưu danh sách layers
        self.layers = layers

    def forward(self, x: list[float]) -> list[float]:
        # TODO: Cho x đi qua lần lượt từng layer và trả về kết quả cuối
        for layer in self.layers:
            x = layer(x)
        return x


class TrackedModel:
    """Đếm tổng số model đã được tạo bằng CLASS attribute.

    - Class attribute `instance_count` (khởi đầu 0): tăng 1 mỗi khi tạo một object mới.
    - __init__(self, name: str): lưu `self.name`, tạo `self.layers` là list RIÊNG của từng object.
    - add_layer(self, layer_name: str) -> None: thêm `layer_name` vào `self.layers`.

    CẨN THẬN: `self.instance_count += 1` KHÔNG sửa class attribute (README mục 1)!
    """
    # TODO: Viết code tại đây
    instance_count = 0
    def __init__(self, name: str):
        self.name = name
        self.layers = []
        TrackedModel.instance_count +=1
    def add_layer(self, layer_name: str) -> None:
        self.layers.append(layer_name)
class StepLRScheduler:
    """Mô phỏng `torch.optim.lr_scheduler.StepLR`.

    - __init__(self, base_lr: float, gamma: float, step_size: int): lưu tham số, `self.epoch = 0`.
    - step(self) -> None: tăng `self.epoch` thêm 1.
    - Thuộc tính CHỈ ĐỌC `lr` (dùng @property, KHÔNG có setter):
        lr = base_lr * gamma ** (epoch // step_size)
    """
    # TODO: Viết code tại đây
    def __init__(self, base_lr: float, gamma: float, step_size: int):
        self.base_lr = base_lr
        self.gamma = gamma
        self.step_size = step_size
        self.epoch = 0
    def step(self) -> None:
        self.epoch +=1
    @property
    def lr(self):
        return self.base_lr * self.gamma ** (self.epoch // self.step_size)

class MiniDataLoader:
    """Mô phỏng `torch.utils.data.DataLoader` (không shuffle).

    - __init__(self, dataset, batch_size: int): `dataset` là bất kỳ object nào có
      `__len__` và `__getitem__` (list, MiniDataset...).
    - __len__(self) -> int: số batch = làm tròn LÊN của len(dataset) / batch_size.
    - __iter__(self): yield lần lượt từng batch; mỗi batch là list các mẫu `dataset[i]`.
      Phải duyệt lại được nhiều lần (mỗi epoch một vòng for)!
    """
    # TODO: Viết code tại đây
    def __init__(self, dataset, batch_size: int):
        self.dataset = dataset
        self.batch_size = batch_size
    def __len__(self) -> int:
        return math.ceil(len(self.dataset) / self.batch_size)
    def __iter__(self):
        for i in range(0, len(self.dataset), self.batch_size):
            yield [self.dataset[j] for j in range(i, min(i + self.batch_size, len(self.dataset)))]
if __name__ == "__main__":
    # Test 1: TrainConfig
    cfg = TrainConfig(epochs=5)
    assert cfg.lr == 1e-3 and cfg.batch_size == 32 and cfg.epochs == 5

    # Test 2: MiniDataset
    ds = MiniDataset([1, 2, 3], [10, 20, 30], transform=lambda v: v * 2)
    assert len(ds) == 3
    assert ds[1] == (4, 20)

    # Test 3: Sequential(Linear1D, ReLU)
    net = Sequential(Linear1D(weight=2.0, bias=-3.0), ReLU())
    # x = [1.0, 2.0, 3.0] -> Linear: [-1.0, 1.0, 3.0] -> ReLU: [0.0, 1.0, 3.0]
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

    print("Module 04: Tất cả bài test đã PASS!")

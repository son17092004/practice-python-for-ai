"""Module 01: Bài tập ôn tập Core Syntax, Mutability & Slicing."""

import copy


def split_train_val_test(
    data: list, train_ratio: float = 0.7, val_ratio: float = 0.15
) -> tuple[list, list, list]:
    """Chia danh sách data thành 3 phần (train, val, test) theo thứ tự bằng slicing.

    Ví dụ: len(data) = 10, train_ratio = 0.7, val_ratio = 0.15
    -> train: 7 phần tử đầu, val: 1 phần tử tiếp theo (int(10 * 0.15) = 1), test: phần còn lại (2).
    """
    # TODO: Viết code tại đây
    len_data = len(data)
    train_end = int(len_data * train_ratio)
    val_end = train_end + int(len_data * val_ratio)
    return (data[:train_end], data[train_end:val_end], data[val_end:]) 


def normalize_matrix_safe(matrix: list[list[float]]) -> list[list[float]]:
    """Trả về ma trận mới với mỗi phần tử chia cho giá trị lớn nhất toàn ma trận.

    QUAN TRỌNG: Không được làm thay đổi `matrix` đầu vào!
    Nếu giá trị lớn nhất là 0, trả về bản sao của matrix ban đầu.
    """
    # TODO: Viết code tại đây
    max_value = max([val for row in matrix for val in row])
    if max_value == 0:
        return copy.deepcopy(matrix)
    matrix_copy = copy.deepcopy(matrix)
    return [[val/max_value for val in row] for row in matrix_copy]

def sliding_windows(sequence: list, window_size: int) -> list[list]:
    """Tạo các cửa sổ trượt (sliding windows) độ dài `window_size` từ `sequence`.

    Ví dụ: sequence = [1, 2, 3, 4, 5], window_size = 3
    -> [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    Nếu window_size > len(sequence) hoặc window_size <= 0, trả về [].
    """
    # TODO: Viết code tại đây
    if window_size > len(sequence) or window_size <= 0:
        return []
    return [sequence[i:i+window_size] for i in range(len(sequence) - window_size + 1)]

def format_training_log(epoch: int, train_loss: float, val_acc: float | None) -> str:
    """Định dạng chuỗi log training:
    - Nếu val_acc is not None: "Epoch 03 | train_loss=0.1234 | val_acc=92.50%" (val_acc nhân 100)
    - Nếu val_acc is None:     "Epoch 03 | train_loss=0.1234 | val_acc=N/A"
    Lưu ý: epoch luôn hiển thị tối thiểu 2 chữ số (ví dụ 3 -> 03), train_loss 4 chữ số thập phân.
    """
    # TODO: Viết code tại đây
    return f"Epoch {epoch:02d} | train_loss={train_loss:.4f} | val_acc={"N/A" if val_acc is None else f"{val_acc:.2%}"}"


def early_stopping_epoch(val_losses: list[float], patience: int) -> int:
    """Mô phỏng Early Stopping: trả về chỉ số epoch (đếm từ 0) mà tại đó training DỪNG.

    Quy tắc:
    - Theo dõi `best` = val_loss nhỏ nhất từ trước tới giờ.
    - Epoch nào có loss < best: cập nhật best và reset bộ đếm `wait` về 0.
    - Ngược lại: tăng `wait` thêm 1. Khi `wait == patience` -> dừng ngay tại epoch đó.
    - Nếu không bao giờ dừng sớm, trả về chỉ số epoch cuối cùng (len - 1).

    Ví dụ: [0.9, 0.7, 0.75, 0.8, 0.6], patience=2 -> 3
    (epoch 2 và 3 không cải thiện so với 0.7 -> wait = 2 tại epoch 3 -> dừng).
    Gợi ý: dùng vòng lặp + `break` (hoặc `return` sớm).
    """
    # TODO: Viết code tại đây
    patience_counter = 0
    len_val_losses = len(val_losses)
    best = float('inf')
    for i,val in enumerate(val_losses):
        if val < best:
            best = val
            patience_counter = 0
        else:
            patience_counter +=1
        if patience_counter == patience:
            return i
    return len_val_losses - 1


def parse_command(command: str) -> str:
    """Phân tích lệnh điều khiển training bằng `match-case` trên `command.split()`.

    - "train <n>" (n là số nguyên dương) -> "Training for <n> epochs"
    - "eval"                             -> "Evaluating"
    - "save <path>"                      -> "Saving to <path>"
    - "quit" hoặc "exit"                 -> "Bye"
    - Mọi trường hợp khác (kể cả "train abc", "save" thiếu path) -> "Unknown command"
    """
    # TODO: Viết code tại đây
    match command.split():
        case ["train",n] if n.isdigit() and int(n) > 0:
            return f"Training for {n} epochs"
        case ["eval"]:
            return "Evaluating"
        case ["save", path]:
            return f"Saving to {path}"
        case "quit" | ["exit"]:
            return "Bye"
        case _:
            return "Unknown command"


if __name__ == "__main__":
    # Test 1: split_train_val_test
    tr, va, te = split_train_val_test(list(range(10)), 0.7, 0.15)
    assert tr == [0, 1, 2, 3, 4, 5, 6]
    assert va == [7]
    assert te == [8, 9]

    # Test 2: normalize_matrix_safe
    orig = [[1.0, 2.0], [3.0, 4.0]]
    norm = normalize_matrix_safe(orig)
    print(norm)
    assert norm == [[0.25, 0.5], [0.75, 1.0]]
    assert orig == [[1.0, 2.0], [3.0, 4.0]], "Không được mutate ma trận gốc!"
    assert normalize_matrix_safe([[0.0, 0.0]]) == [[0.0, 0.0]]

    # Test 3: sliding_windows
    assert sliding_windows([1, 2, 3, 4, 5], 3) == [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    assert sliding_windows([1, 2], 3) == []

    # Test 4: format_training_log
    assert format_training_log(3, 0.12344, 0.925) == "Epoch 03 | train_loss=0.1234 | val_acc=92.50%"
    assert format_training_log(12, 0.5, None) == "Epoch 12 | train_loss=0.5000 | val_acc=N/A"

    # Test 5: early_stopping_epoch
    assert early_stopping_epoch([0.9, 0.7, 0.75, 0.8, 0.6], patience=2) == 3
    assert early_stopping_epoch([0.9, 0.8, 0.7, 0.6], patience=2) == 3, "Không dừng sớm -> epoch cuối"
    assert early_stopping_epoch([0.5, 0.6, 0.4, 0.45, 0.5, 0.55], patience=3) == 5
    assert early_stopping_epoch([0.5, 0.5], patience=1) == 1, "Bằng nhau KHÔNG tính là cải thiện"

    # Test 6: parse_command
    assert parse_command("train 5") == "Training for 5 epochs"
    assert parse_command("eval") == "Evaluating"
    assert parse_command("save model.pt") == "Saving to model.pt"
    assert parse_command("exit") == "Bye"
    assert parse_command("train abc") == "Unknown command"
    assert parse_command("train 0") == "Unknown command"
    assert parse_command("save") == "Unknown command"
    assert parse_command("") == "Unknown command"

    print("Module 01: Tất cả bài test đã PASS!")

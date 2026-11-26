"""Module 01: Lời giải tham khảo."""

import copy


def split_train_val_test(
    data: list, train_ratio: float = 0.7, val_ratio: float = 0.15
) -> tuple[list, list, list]:
    n = len(data)
    train_end = int(n * train_ratio)
    val_end = train_end + int(n * val_ratio)
    return data[:train_end], data[train_end:val_end], data[val_end:]


def normalize_matrix_safe(matrix: list[list[float]]) -> list[list[float]]:
    if not matrix or not matrix[0]:
        return copy.deepcopy(matrix)

    max_val = max(val for row in matrix for val in row)
    if max_val == 0:
        return copy.deepcopy(matrix)

    return [[val / max_val for val in row] for row in matrix]


def sliding_windows(sequence: list, window_size: int) -> list[list]:
    if window_size <= 0 or window_size > len(sequence):
        return []
    return [sequence[i : i + window_size] for i in range(len(sequence) - window_size + 1)]


def format_training_log(epoch: int, train_loss: float, val_acc: float | None) -> str:
    acc_str = f"{val_acc * 100:.2f}%" if val_acc is not None else "N/A"
    return f"Epoch {epoch:02d} | train_loss={train_loss:.4f} | val_acc={acc_str}"


def early_stopping_epoch(val_losses: list[float], patience: int) -> int:
    best = float("inf")
    wait = 0
    for epoch, loss in enumerate(val_losses):
        if loss < best:
            best, wait = loss, 0
            continue
        wait += 1
        if wait == patience:
            return epoch
    return len(val_losses) - 1


def parse_command(command: str) -> str:
    match command.split():
        case ["train", n] if n.isdigit() and int(n) > 0:
            return f"Training for {n} epochs"
        case ["eval"]:
            return "Evaluating"
        case ["save", path]:
            return f"Saving to {path}"
        case ["quit" | "exit"]:
            return "Bye"
        case _:
            return "Unknown command"


if __name__ == "__main__":
    tr, va, te = split_train_val_test(list(range(10)), 0.7, 0.15)
    assert tr == [0, 1, 2, 3, 4, 5, 6]
    assert va == [7]
    assert te == [8, 9]

    orig = [[1.0, 2.0], [3.0, 4.0]]
    norm = normalize_matrix_safe(orig)
    assert norm == [[0.25, 0.5], [0.75, 1.0]]
    assert orig == [[1.0, 2.0], [3.0, 4.0]]
    assert normalize_matrix_safe([[0.0, 0.0]]) == [[0.0, 0.0]]

    assert sliding_windows([1, 2, 3, 4, 5], 3) == [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    assert sliding_windows([1, 2], 3) == []

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

    print("Module 01 (solutions): Tất cả bài test đã PASS!")

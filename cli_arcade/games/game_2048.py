from __future__ import annotations
import random

SIZE = 4

def _empty_cells(board: list[list[int]]) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 0:
                out.append((r, c))
    return out

def _spawn(board: list[list[int]]) -> None:
    empties = _empty_cells(board)
    if not empties:
        return
    r, c = random.choice(empties)
    board[r][c] = 4 if random.random() < 0.10 else 2

def _compress_merge_left(row: list[int]) -> tuple[list[int], int]:
    """
    Returns (new_row, gained_score).
    2048 merge rules: merge equal neighbors once per move.
    """
    vals = [x for x in row if x != 0]
    out: list[int] = []
    gained = 0
    i = 0
    while i < len(vals):
        if i + 1 < len(vals) and vals[i] == vals[i + 1]:
            merged = vals[i] * 2
            out.append(merged)
            gained += merged
            i += 2
        else:
            out.append(vals[i])
            i += 1
    out.extend([0] * (SIZE - len(out)))
    return out, gained

def _move_left(board: list[list[int]]) -> tuple[list[list[int]], bool, int]:
    new_board: list[list[int]] = []
    moved = False
    gained_total = 0
    for r in range(SIZE):
        new_row, gained = _compress_merge_left(board[r])
        gained_total += gained
        if new_row != board[r]:
            moved = True
        new_board.append(new_row)
    return new_board, moved, gained_total

def _reverse_rows(board: list[list[int]]) -> list[list[int]]:
    return [list(reversed(row)) for row in board]

def _transpose(board: list[list[int]]) -> list[list[int]]:
    return [list(col) for col in zip(*board)]

def _any_2048(board: list[list[int]]) -> bool:
    return any(2048 in row for row in board)

def _can_move(board: list[list[int]]) -> bool:
    if _empty_cells(board):
        return True
    # check horizontal
    for r in range(SIZE):
        for c in range(SIZE - 1):
            if board[r][c] == board[r][c + 1]:
                return True
    # check vertical
    for c in range(SIZE):
        for r in range(SIZE - 1):
            if board[r][c] == board[r + 1][c]:
                return True
    return False

def _clear_screen() -> None:
    # simple ANSI clear (works in most terminals)
    print("\033[2J\033[H", end="")

def _print_board(board: list[list[int]], score: int) -> None:
    _clear_screen()
    print("🎮 2048")
    print("Controls: w/a/s/d move | q quit\n")
    print(f"Score: {score}\n")

    width = 5
    line = "+" + "+".join(["-" * width] * SIZE) + "+"
    print(line)
    for r in range(SIZE):
        row = []
        for c in range(SIZE):
            v = board[r][c]
            row.append(str(v).rjust(width) if v != 0 else " ".rjust(width))
        print("|" + "|".join(row) + "|")
        print(line)

def play_2048() -> int:
    """
    Returns:
      1 -> win (reach 2048)
      0 -> loss/quit
    """
    board = [[0] * SIZE for _ in range(SIZE)]
    score = 0
    _spawn(board)
    _spawn(board)

    while True:
        _print_board(board, score)

        if _any_2048(board):
            print("\n✅ You reached 2048! You win!\n")
            return 1

        if not _can_move(board):
            print("\n❌ No moves left. Game over.\n")
            return 0

        cmd = input("Move: ").strip().lower()
        if cmd == "q":
            print("\nBye!\n")
            return 0
        if cmd not in ("w", "a", "s", "d"):
            continue

        moved = False
        gained = 0
        new_board = board

        if cmd == "a":
            new_board, moved, gained = _move_left(board)
        elif cmd == "d":
            rb = _reverse_rows(board)
            rb2, moved, gained = _move_left(rb)
            new_board = _reverse_rows(rb2)
        elif cmd == "w":
            tb = _transpose(board)
            tb2, moved, gained = _move_left(tb)
            new_board = _transpose(tb2)
        elif cmd == "s":
            tb = _transpose(board)
            rb = _reverse_rows(tb)
            rb2, moved, gained = _move_left(rb)
            new_board = _transpose(_reverse_rows(rb2))

        if moved:
            board = new_board
            score += gained
            _spawn(board)

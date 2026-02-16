from __future__ import annotations
import random

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6),             # diagonals
]

def _winner(board: list[str]) -> str | None:
    for a, b, c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None

def _is_draw(board: list[str]) -> bool:
    return _winner(board) is None and all(x != " " for x in board)

def _render(board: list[str]) -> None:
    def cell(i: int) -> str:
        return board[i] if board[i] != " " else str(i + 1)

    print()
    print(f" {cell(0)} | {cell(1)} | {cell(2)} ")
    print("---+---+---")
    print(f" {cell(3)} | {cell(4)} | {cell(5)} ")
    print("---+---+---")
    print(f" {cell(6)} | {cell(7)} | {cell(8)} ")
    print()

def _available_moves(board: list[str]) -> list[int]:
    return [i for i, v in enumerate(board) if v == " "]

def _try_win(board: list[str], mark: str) -> int | None:
    # return a move index that wins immediately, else None
    for i in _available_moves(board):
        board[i] = mark
        if _winner(board) == mark:
            board[i] = " "
            return i
        board[i] = " "
    return None

def _cpu_move(board: list[str], cpu: str, human: str) -> int:
    # 1) win if possible
    m = _try_win(board, cpu)
    if m is not None:
        return m

    # 2) block human win
    m = _try_win(board, human)
    if m is not None:
        return m

    # 3) take center
    if board[4] == " ":
        return 4

    # 4) take corners
    corners = [0, 2, 6, 8]
    free_corners = [c for c in corners if board[c] == " "]
    if free_corners:
        return random.choice(free_corners)

    # 5) take sides
    sides = [1, 3, 5, 7]
    free_sides = [s for s in sides if board[s] == " "]
    if free_sides:
        return random.choice(free_sides)

    # fallback
    return random.choice(_available_moves(board))

def play_tic_tac_toe() -> int:
    """
    Returns:
      1  -> player X win (counts as win)
      0  -> loss / quit
     -1  -> draw
    """
    board = [" "] * 9

    print("\n🎮 Tic Tac Toe")
    print("Pick 1-9 to place. Type 'q' to quit.\n")
    print("Mode: 1) vs CPU  2) two-player")
    mode = input("Choose (default 1): ").strip().lower()
    two_player = (mode == "2")

    human = "X"
    cpu = "O"

    turn = "X"
    while True:
        _render(board)

        w = _winner(board)
        if w is not None:
            print(f"🏆 {w} wins!\n")
            if two_player:
                return 1 if w == "X" else 0
            return 1 if w == human else 0

        if _is_draw(board):
            print("🤝 Draw.\n")
            return -1

        if not two_player and turn == cpu:
            move = _cpu_move(board, cpu=cpu, human=human)
            board[move] = cpu
            turn = human
            continue

        raw = input(f"{turn}'s move (1-9): ").strip().lower()
        if raw == "q":
            print("Bye!\n")
            return 0
        if not raw.isdigit():
            print("Invalid input.\n")
            continue

        pos = int(raw)
        if pos < 1 or pos > 9:
            print("Pick a number from 1 to 9.\n")
            continue

        idx = pos - 1
        if board[idx] != " ":
            print("That spot is taken.\n")
            continue

        board[idx] = turn
        turn = "O" if turn == "X" else "X"

from __future__ import annotations
import random
import time
from typing import Optional

# Grid size (inside the border)
W = 24
H = 14
TARGET_LEN = 20  # reach this length to "win"

DIRS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}

OPPOSITE = {
    "UP": "DOWN",
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "RIGHT": "LEFT",
}

def _rand_food(snake: list[tuple[int, int]]) -> tuple[int, int]:
    occupied = set(snake)
    empties = [(x, y) for x in range(W) for y in range(H) if (x, y) not in occupied]
    return random.choice(empties) if empties else (-1, -1)

def _step(snake: list[tuple[int, int]], direction: str, food: tuple[int, int]) -> tuple[list[tuple[int, int]], tuple[int, int], bool, bool]:
    """
    Returns: (snake, food, ate, dead)
    """
    dx, dy = DIRS[direction]
    hx, hy = snake[0]
    new_head = (hx + dx, hy + dy)

    # wall collision
    if not (0 <= new_head[0] < W and 0 <= new_head[1] < H):
        return snake, food, False, True

    grow = (new_head == food)

    # self collision:
    # if not growing, tail moves away, so allow stepping into current tail cell
    body_to_check = snake if grow else snake[:-1]
    if new_head in body_to_check:
        return snake, food, False, True

    new_snake = [new_head] + snake
    if not grow:
        new_snake.pop()  # remove tail
        return new_snake, food, False, False

    # grow -> spawn new food
    new_food = _rand_food(new_snake)
    return new_snake, new_food, True, False

def _play_turn_based() -> int:
    snake = [(W // 2, H // 2), (W // 2 - 1, H // 2), (W // 2 - 2, H // 2)]
    direction = "RIGHT"
    food = _rand_food(snake)

    def render() -> None:
        print("\033[2J\033[H", end="")
        print("🎮 Snake (turn-based fallback)")
        print("Controls: w/a/s/d move | Enter repeats direction | q quit")
        print(f"Length: {len(snake)}  Target: {TARGET_LEN}\n")

        border = "+" + "-" * W + "+"
        print(border)
        sset = set(snake)
        for y in range(H):
            row = []
            for x in range(W):
                if (x, y) == snake[0]:
                    row.append("O")
                elif (x, y) in sset:
                    row.append("o")
                elif (x, y) == food:
                    row.append("*")
                else:
                    row.append(" ")
            print("|" + "".join(row) + "|")
        print(border)

    keymap = {"w": "UP", "s": "DOWN", "a": "LEFT", "d": "RIGHT"}

    while True:
        render()
        if len(snake) >= TARGET_LEN:
            print("\n✅ You reached the target length! You win!\n")
            return 1

        cmd = input("Move: ").strip().lower()
        if cmd == "q":
            print("\nBye!\n")
            return 0

        if cmd in keymap:
            nd = keymap[cmd]
            if nd != OPPOSITE[direction]:
                direction = nd

        snake, food, _, dead = _step(snake, direction, food)
        if dead:
            render()
            print("\n❌ Game over.\n")
            return 0

def _play_curses() -> int:
    import curses  # noqa: F401

    def run(stdscr) -> int:
        import curses

        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.keypad(True)

        snake = [(W // 2, H // 2), (W // 2 - 1, H // 2), (W // 2 - 2, H // 2)]
        direction = "RIGHT"
        food = _rand_food(snake)

        delay = 0.12  # seconds per tick

        keymap = {
            curses.KEY_UP: "UP",
            curses.KEY_DOWN: "DOWN",
            curses.KEY_LEFT: "LEFT",
            curses.KEY_RIGHT: "RIGHT",
            ord("w"): "UP",
            ord("s"): "DOWN",
            ord("a"): "LEFT",
            ord("d"): "RIGHT",
        }

        last_tick = time.perf_counter()

        while True:
            # input
            k = stdscr.getch()
            if k in (ord("q"), ord("Q")):
                return 0
            if k in keymap:
                nd = keymap[k]
                if nd != OPPOSITE[direction]:
                    direction = nd

            now = time.perf_counter()
            if now - last_tick < delay:
                time.sleep(0.005)
                continue
            last_tick = now

            snake, food, ate, dead = _step(snake, direction, food)
            if ate:
                delay = max(0.06, delay * 0.97)

            # draw
            stdscr.erase()
            stdscr.addstr(0, 0, "🎮 Snake  |  WASD/Arrows move  |  q quit")
            stdscr.addstr(1, 0, f"Length: {len(snake)}  Target: {TARGET_LEN}")

            # border
            top = 3
            left = 0
            stdscr.addstr(top, left, "+" + "-" * W + "+")
            for y in range(H):
                stdscr.addstr(top + 1 + y, left, "|" + " " * W + "|")
            stdscr.addstr(top + 1 + H, left, "+" + "-" * W + "+")

            # food
            fx, fy = food
            if 0 <= fx < W and 0 <= fy < H:
                stdscr.addch(top + 1 + fy, 1 + fx, ord("*"))

            # snake
            for i, (x, y) in enumerate(snake):
                ch = "O" if i == 0 else "o"
                stdscr.addch(top + 1 + y, 1 + x, ord(ch))

            stdscr.refresh()

            if dead:
                stdscr.nodelay(False)
                stdscr.addstr(top + 3 + H, 0, "❌ Game over. Press any key...")
                stdscr.getch()
                return 0

            if len(snake) >= TARGET_LEN:
                stdscr.nodelay(False)
                stdscr.addstr(top + 3 + H, 0, "✅ You win! Press any key...")
                stdscr.getch()
                return 1

    import curses
    return curses.wrapper(run)

def play_snake() -> int:
    """
    Returns:
      1 -> win (reach TARGET_LEN)
      0 -> loss/quit
    """
    try:
        return _play_curses()
    except Exception:
        # if curses fails for any reason, fall back to turn-based
        return _play_turn_based()

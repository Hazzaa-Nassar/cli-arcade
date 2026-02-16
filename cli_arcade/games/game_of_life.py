from __future__ import annotations
import random
import time

W = 40
H = 20

TARGET_GENS = 200
LOOP_MEMORY = 50

ALIVE = "█"
DEAD = " "

def _blank() -> list[list[int]]:
    return [[0] * W for _ in range(H)]

def _randomize(board: list[list[int]], p: float = 0.28) -> None:
    for y in range(H):
        for x in range(W):
            board[y][x] = 1 if random.random() < p else 0

def _stamp(board: list[list[int]], cells: list[tuple[int, int]], ox: int, oy: int) -> None:
    for x, y in cells:
        xx, yy = ox + x, oy + y
        if 0 <= xx < W and 0 <= yy < H:
            board[yy][xx] = 1

def _pattern(name: str) -> list[tuple[int, int]]:
    if name == "glider":
        return [(1,0),(2,1),(0,2),(1,2),(2,2)]
    if name == "blinker":
        return [(0,0),(1,0),(2,0)]
    if name == "toad":
        return [(1,0),(2,0),(3,0),(0,1),(1,1),(2,1)]
    if name == "beacon":
        return [(0,0),(1,0),(0,1),(3,2),(2,3),(3,3)]
    return []

def _count_alive(board: list[list[int]]) -> int:
    return sum(sum(row) for row in board)

def _hash(board: list[list[int]]) -> str:
    return "".join("".join("1" if c else "0" for c in row) for row in board)

def _step(board: list[list[int]]) -> list[list[int]]:
    nb = _blank()
    for y in range(H):
        for x in range(W):
            n = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    yy, xx = y + dy, x + dx
                    if 0 <= xx < W and 0 <= yy < H:
                        n += board[yy][xx]
            if board[y][x] == 1:
                nb[y][x] = 1 if (n == 2 or n == 3) else 0
            else:
                nb[y][x] = 1 if n == 3 else 0
    return nb

def _fallback_text() -> int:
    board = _blank()
    _randomize(board)
    gen = 0
    speed = 0.08
    history: list[str] = []
    auto = False

    def render() -> None:
        print("\033[2J\033[H", end="")
        print("🎮 Conway's Game of Life (text fallback)")
        print("Enter=step | space=auto | r=random | c=clear | g=glider | b=blinker | t=toad | q quit")
        print(f"Gen: {gen} | Alive: {_count_alive(board)} | Win@{TARGET_GENS}\n")
        for row in board:
            print("".join(ALIVE if c else DEAD for c in row))

    while True:
        render()
        alive = _count_alive(board)

        if alive == 0:
            print("\n❌ Everything died.\n")
            return 0
        if gen >= TARGET_GENS:
            print("\n✅ Still alive at target gen! You win!\n")
            return 1

        h = _hash(board)
        history.append(h)
        if len(history) > LOOP_MEMORY:
            history.pop(0)
        if history.count(h) > 1:
            print("\n🤝 Pattern is repeating (loop). Draw.\n")
            return -1

        if auto:
            time.sleep(speed)
            board = _step(board)
            gen += 1
            continue

        cmd = input("\ncmd: ")
        if cmd.strip().lower() == "q":
            print("\nBye!\n")
            return 0
        if cmd == " ":
            auto = True
            continue

        c = cmd.strip().lower()
        if c == "r":
            _randomize(board)
            gen = 0
        elif c == "c":
            board = _blank()
            gen = 0
        elif c in ("g", "b", "t"):
            board = _blank()
            pat = {"g":"glider","b":"blinker","t":"toad"}[c]
            _stamp(board, _pattern(pat), W // 2, H // 2)
            gen = 0
        else:
            board = _step(board)
            gen += 1

def _curses_mode() -> int:
    import curses

    def run(stdscr) -> int:
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.keypad(True)

        board = _blank()
        _randomize(board)
        gen = 0
        speed = 0.08
        paused = False
        history: list[str] = []

        while True:
            alive = _count_alive(board)

            # end conditions
            if alive == 0:
                stdscr.nodelay(False)
                stdscr.addstr(H + 4, 0, "❌ Everything died. Press any key...")
                stdscr.getch()
                return 0
            if gen >= TARGET_GENS:
                stdscr.nodelay(False)
                stdscr.addstr(H + 4, 0, "✅ Still alive at target gen! You win! Press any key...")
                stdscr.getch()
                return 1

            # loop detection
            h = _hash(board)
            history.append(h)
            if len(history) > LOOP_MEMORY:
                history.pop(0)
            if history.count(h) > 1:
                stdscr.nodelay(False)
                stdscr.addstr(H + 4, 0, "🤝 Pattern repeating. Draw. Press any key...")
                stdscr.getch()
                return -1

            # input
            k = stdscr.getch()
            if k in (ord("q"), ord("Q")):
                return 0
            if k == ord(" "):
                paused = not paused
            if k in (ord("r"), ord("R")):
                _randomize(board)
                gen = 0
            if k in (ord("c"), ord("C")):
                board = _blank()
                gen = 0
            if k in (ord("g"), ord("G")):
                board = _blank()
                _stamp(board, _pattern("glider"), W // 2, H // 2)
                gen = 0
            if k in (ord("b"), ord("B")):
                board = _blank()
                _stamp(board, _pattern("blinker"), W // 2, H // 2)
                gen = 0
            if k in (ord("t"), ord("T")):
                board = _blank()
                _stamp(board, _pattern("toad"), W // 2, H // 2)
                gen = 0
            if k in (ord("+"), ord("=")):
                speed = max(0.02, speed * 0.8)
            if k == ord("-"):
                speed = min(0.5, speed * 1.25)

            # draw
            stdscr.erase()
            stdscr.addstr(0, 0, "🎮 Game of Life | space=pause | r=random c=clear g/b/t patterns | +/- speed | q quit")
            stdscr.addstr(1, 0, f"Gen: {gen} | Alive: {alive} | speed: {speed:.2f}s | Win@{TARGET_GENS} | {'PAUSED' if paused else 'RUNNING'}")

            top = 3
            for y in range(H):
                row = "".join(ALIVE if board[y][x] else DEAD for x in range(W))
                stdscr.addstr(top + y, 0, row)

            stdscr.refresh()

            if not paused:
                time.sleep(speed)
                board = _step(board)
                gen += 1
            else:
                time.sleep(0.02)

    return curses.wrapper(run)

def play_life() -> int:
    try:
        return _curses_mode()
    except Exception:
        return _fallback_text()

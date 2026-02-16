from __future__ import annotations
import argparse

from cli_arcade.registry import GAMES, get_game
from cli_arcade.storage import load_progress, save_progress, record_result

def cmd_list() -> int:
    print("\nAvailable games:\n")
    for g in GAMES:
        print(f"- {g.id}: {g.name} — {g.description}")
    print()
    return 0

def cmd_stats() -> int:
    progress = load_progress()
    games = progress.get("games", {})
    print("\nStats:\n")
    if not games:
        print("No games played yet.\n")
        return 0

    for g in GAMES:
        s = games.get(g.id, {"played": 0, "wins": 0, "draws": 0})
        print(f"- {g.name}: played={s['played']} wins={s['wins']} draws={s.get('draws', 0)}")
    print()
    return 0

def cmd_play(game_id: str) -> int:
    game = get_game(game_id)
    if not game:
        print(f"Unknown game_id: {game_id}")
        print("Use: python -m cli_arcade list")
        return 2

    progress = load_progress()
    result = game.play()
    wins = 1 if result == 1 else 0
    draws = 1 if result == -1 else 0
    record_result(progress, game_id, played=1, wins=wins, draws=draws)
    save_progress(progress)
    return 0

def interactive_menu() -> int:
    while True:
        print("\n=== CLI Arcade ===")
        for i, g in enumerate(GAMES, start=1):
            print(f"{i}) {g.id} — {g.name}")
        print("S) Stats")
        print("Q) Quit")
        print("\nTip: you can type a number (1) or a game id (rps).")

        choice = input("\nChoose: ").strip().lower()
        if choice == "q":
            return 0
        if choice == "s":
            cmd_stats()
            continue

        # allow selecting by number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(GAMES):
                cmd_play(GAMES[idx].id)
                continue

        # allow selecting by game id
        game = get_game(choice)
        if game:
            cmd_play(game.id)
            continue

        print("Invalid choice. Try again.\n")
def main() -> int:
    p = argparse.ArgumentParser(prog="cli_arcade", description="A tiny terminal arcade.")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("list")
    sub.add_parser("stats")

    play_p = sub.add_parser("play")
    play_p.add_argument("game_id")

    args = p.parse_args()

    if args.cmd == "list":
        return cmd_list()
    if args.cmd == "stats":
        return cmd_stats()
    if args.cmd == "play":
        return cmd_play(args.game_id)

    return interactive_menu()

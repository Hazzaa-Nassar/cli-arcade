from __future__ import annotations
from dataclasses import dataclass
from typing import Callable

from cli_arcade.games.guess_number import play_guess_number
from cli_arcade.games.rock_paper_scissors import play_rps

@dataclass(frozen=True)
class Game:
    id: str
    name: str
    description: str
    play: Callable[[], int]  # returns 1 if win else 0

GAMES: list[Game] = [
    Game(
        id="guess_number",
        name="Guess the Number",
        description="Guess a secret number in limited attempts.",
        play=play_guess_number,
    ),
    Game(
        id="rps",
        name="Rock Paper Scissors",
        description="Classic RPS vs the computer.",
        play=play_rps,
    ),
]

def get_game(game_id: str) -> Game | None:
    for g in GAMES:
        if g.id == game_id:
            return g
    return None

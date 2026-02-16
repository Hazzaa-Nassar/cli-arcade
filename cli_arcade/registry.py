from __future__ import annotations
from dataclasses import dataclass
from typing import Callable

from cli_arcade.games.guess_number import play_guess_number
from cli_arcade.games.rock_paper_scissors import play_rps
from cli_arcade.games.tic_tac_toe import play_tic_tac_toe
from cli_arcade.games.math_quiz import play_math_quiz
from cli_arcade.games.dice_poker import play_dice_poker
from cli_arcade.games.blackjack import play_blackjack

@dataclass(frozen=True)
class Game:
    id: str
    name: str
    description: str
    play: Callable[[], int]  # 1 win, 0 loss/quit, -1 draw (some games)

GAMES: list[Game] = [
    Game("guess_number", "Guess the Number", "Guess a secret number in limited attempts.", play_guess_number),
    Game("rps", "Rock Paper Scissors", "Classic RPS vs the computer.", play_rps),
    Game("ttt", "Tic Tac Toe", "Play tic tac toe (CPU or 2-player).", play_tic_tac_toe),
    Game("math_quiz", "Math Quiz", "5 quick math questions. Score 4+ to win.", play_math_quiz),
    Game("dice_poker", "Dice Poker", "Roll 5 dice and beat the dealer (poker-style hands).", play_dice_poker),
    Game("blackjack", "Blackjack", "Beat the dealer without going over 21.", play_blackjack),
]

def get_game(game_id: str) -> Game | None:
    for g in GAMES:
        if g.id == game_id:
            return g
    return None

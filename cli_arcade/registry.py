from __future__ import annotations
from dataclasses import dataclass
from typing import Callable

from cli_arcade.games.guess_number import play_guess_number
from cli_arcade.games.rock_paper_scissors import play_rps
from cli_arcade.games.tic_tac_toe import play_tic_tac_toe
from cli_arcade.games.math_quiz import play_math_quiz

from cli_arcade.games.hangman import play_hangman
from cli_arcade.games.word_scramble import play_scramble
from cli_arcade.games.bulls_and_cows import play_bulls_cows

@dataclass(frozen=True)
class Game:
    id: str
    name: str
    description: str
    play: Callable[[], int]  # returns 1 win, 0 loss/quit, -1 draw (some games)

GAMES: list[Game] = [
    Game("guess_number", "Guess the Number", "Guess a secret number in limited attempts.", play_guess_number),
    Game("rps", "Rock Paper Scissors", "Classic RPS vs the computer.", play_rps),
    Game("ttt", "Tic Tac Toe", "Play tic tac toe (CPU or 2-player).", play_tic_tac_toe),
    Game("math_quiz", "Math Quiz", "5 quick math questions. Score 4+ to win.", play_math_quiz),

    Game("hangman", "Hangman", "Guess the word, one letter at a time.", play_hangman),
    Game("scramble", "Word Scramble", "Unscramble the word in 3 attempts.", play_scramble),
    Game("bulls_cows", "Bulls & Cows", "Crack the 4-digit code with hints.", play_bulls_cows),
]

def get_game(game_id: str) -> Game | None:
    for g in GAMES:
        if g.id == game_id:
            return g
    return None

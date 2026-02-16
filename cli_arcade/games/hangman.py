from __future__ import annotations
import random

WORDS = [
    "python", "terminal", "arcade", "program", "debug", "system", "memory",
    "version", "package", "string", "integer", "function", "module", "variable",
    "compile", "testing", "syntax", "object", "random", "github", "linux", "ubuntu",
    "coding", "design", "logic", "thread", "array", "window", "wsl", "engine",
]

def _masked(word: str, guessed: set[str]) -> str:
    return " ".join([c if c in guessed else "_" for c in word])

def play_hangman() -> int:
    """
    Returns:
      1 -> win
      0 -> loss/quit
    """
    word = random.choice(WORDS)
    guessed: set[str] = set()
    wrong: set[str] = set()
    tries = 6

    print("\n🎮 Hangman")
    print("Guess letters (or guess the full word). Type 'q' to quit.\n")

    while True:
        print(f"Word: {_masked(word, guessed)}")
        if wrong:
            print(f"Wrong: {' '.join(sorted(wrong))}")
        print(f"Tries left: {tries}\n")

        # win check
        if all(c in guessed for c in word):
            print("✅ You guessed it!\n")
            return 1

        # lose check
        if tries <= 0:
            print(f"❌ You lost. Word was: {word}\n")
            return 0

        g = input("Guess: ").strip().lower()
        if g == "q":
            print("Bye!\n")
            return 0

        if not g.isalpha():
            print("Letters only.\n")
            continue

        # full word guess
        if len(g) > 1:
            if g == word:
                print("✅ Correct! You win!\n")
                return 1
            tries -= 1
            print("❌ Wrong word.\n")
            continue

        # single letter guess
        ch = g
        if ch in guessed or ch in wrong:
            print("Already guessed.\n")
            continue

        if ch in word:
            guessed.add(ch)
            print("✅ Nice.\n")
        else:
            wrong.add(ch)
            tries -= 1
            print("❌ Nope.\n")

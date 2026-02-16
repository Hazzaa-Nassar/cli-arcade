from __future__ import annotations
import random

WORDS = [
    "python", "terminal", "arcade", "program", "debug", "network", "system",
    "memory", "version", "package", "string", "integer", "function", "module",
    "variable", "compile", "testing", "syntax", "object", "random", "github",
    "linux", "ubuntu", "wsl", "coding", "design", "logic", "thread", "array",
]

def _mask(word: str, guessed: set[str]) -> str:
    return " ".join([c if c in guessed else "_" for c in word])

def play_hangman() -> int:
    word = random.choice(WORDS)
    guessed: set[str] = set()
    wrong: set[str] = set()
    tries = 6

    print("\n🎮 Hangman")
    print("Guess letters. You can also guess the full word.")
    print("Type 'q' to quit.\n")

    while True:
        masked = _mask(word, guessed)
        print(f"Word: {masked}")
        if wrong:
            print(f"Wrong: {' '.join(sorted(wrong))}")
        print(f"Tries left: {tries}\n")

        if "_" not in masked.replace(" ", ""):
            print("✅ You guessed it!\n")
            return 1

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
            else:
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

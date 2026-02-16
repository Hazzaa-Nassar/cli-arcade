from __future__ import annotations
import random

WORDS = [
    "computer", "keyboard", "terminal", "developer", "function", "internet",
    "variable", "package", "compile", "testing", "debugging", "algorithm",
]

def _scramble(word: str) -> str:
    if len(word) <= 2:
        return word
    letters = list(word)
    for _ in range(20):
        random.shuffle(letters)
        s = "".join(letters)
        if s != word:
            return s
    return "".join(letters)

def play_scramble() -> int:
    word = random.choice(WORDS)
    scrambled = _scramble(word)
    attempts = 3

    print("\n🎮 Word Scramble")
    print("Unscramble the word. Type 'hint' for first letter. Type 'q' to quit.\n")
    print(f"Scrambled: {scrambled} (length={len(word)})\n")

    hinted = False
    for i in range(1, attempts + 1):
        g = input(f"Attempt {i}/{attempts}: ").strip().lower()
        if g == "q":
            print("Bye!\n")
            return 0
        if g == "hint":
            if not hinted:
                print(f"Hint: starts with '{word[0]}'\n")
                hinted = True
            else:
                print("Hint already used.\n")
            continue

        if g == word:
            print("✅ Correct! You win!\n")
            return 1
        print("❌ Wrong.\n")

    print(f"Out of attempts. The word was: {word}\n")
    return 0

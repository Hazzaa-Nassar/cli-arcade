from __future__ import annotations
import random
from collections import Counter

# Simple built-in list (stdlib only). You can expand later.
WORDS = [
    "crate","slate","trace","stare","raise","arise","react","cared","cable","table",
    "smile","pride","spice","grace","shade","flame","plane","stone","crown","brown",
    "skill","build","guess","poker","black","sharp","buzzy","jazzy","fuzzy","eager",
    "sugar","tiger","zebra","apple","mango","peach","lemon","grape","berry","chill",
    "witty","trust","light","night","sound","minor","major","break","fresh","clean",
]

GREEN = "🟩"
YELLOW = "🟨"
BLACK = "⬛"

def _score(secret: str, guess: str) -> str:
    # Wordle-like scoring with duplicate handling
    res = [BLACK] * 5

    secret_counts = Counter(secret)

    # 1) greens
    for i in range(5):
        if guess[i] == secret[i]:
            res[i] = GREEN
            secret_counts[guess[i]] -= 1

    # 2) yellows
    for i in range(5):
        if res[i] == GREEN:
            continue
        ch = guess[i]
        if secret_counts[ch] > 0:
            res[i] = YELLOW
            secret_counts[ch] -= 1

    return "".join(res)

def play_wordle_lite() -> int:
    """
    Returns:
      1 -> win
      0 -> loss/quit
    """
    secret = random.choice(WORDS)
    tries = 6

    print("\n🎮 Wordle-lite")
    print("Guess the 5-letter word. You have 6 tries.")
    print("🟩 correct spot, 🟨 wrong spot, ⬛ not in word")
    print("Type 'q' to quit.\n")

    history: list[tuple[str, str]] = []

    for t in range(1, tries + 1):
        # show history
        if history:
            for g, s in history:
                print(f"{g.upper()}  {s}")
            print()

        guess = input(f"Try {t}/{tries}: ").strip().lower()
        if guess == "q":
            print("Bye!\n")
            return 0

        if len(guess) != 5 or (not guess.isalpha()):
            print("Enter exactly 5 letters.\n")
            continue

        score = _score(secret, guess)
        history.append((guess, score))

        if guess == secret:
            print(f"\n{guess.upper()}  {score}")
            print("✅ You got it!\n")
            return 1

    print()
    for g, s in history:
        print(f"{g.upper()}  {s}")
    print(f"\n❌ Out of tries. The word was: {secret.upper()}\n")
    return 0

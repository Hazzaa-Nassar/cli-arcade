from __future__ import annotations
import random

def _secret_code() -> str:
    # 4 unique digits
    digits = random.sample("0123456789", 4)
    return "".join(digits)

def _score(secret: str, guess: str) -> tuple[int, int]:
    bulls = sum(1 for i in range(4) if guess[i] == secret[i])
    cows = sum(1 for ch in guess if ch in secret) - bulls
    return bulls, cows

def play_bulls_cows() -> int:
    secret = _secret_code()
    attempts = 10

    print("\n🎮 Bulls & Cows")
    print("Guess the 4-digit code (all digits unique).")
    print("Bulls = correct digit in correct place.")
    print("Cows  = correct digit in wrong place.")
    print("Type 'q' to quit.\n")

    for i in range(1, attempts + 1):
        g = input(f"Attempt {i}/{attempts}: ").strip().lower()
        if g == "q":
            print("Bye!\n")
            return 0
        if len(g) != 4 or (not g.isdigit()):
            print("Enter exactly 4 digits.\n")
            continue
        if len(set(g)) != 4:
            print("Digits must be unique.\n")
            continue

        bulls, cows = _score(secret, g)
        if bulls == 4:
            print("✅ Perfect! You cracked it!\n")
            return 1

        print(f"Bulls: {bulls}, Cows: {cows}\n")

    print(f"❌ Out of attempts. Code was: {secret}\n")
    return 0

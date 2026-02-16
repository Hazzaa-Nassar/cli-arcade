from __future__ import annotations
import random

def play_guess_number() -> int:
    secret = random.randint(1, 20)
    attempts = 5

    print("\n🎮 Guess the Number")
    print("I picked a number from 1 to 20.")
    print(f"You have {attempts} attempts.\n")

    for i in range(1, attempts + 1):
        raw = input(f"Attempt {i}/{attempts} - your guess: ").strip()
        if not raw.isdigit():
            print("Please enter a valid integer.\n")
            continue

        guess = int(raw)
        if guess == secret:
            print("✅ Correct! You win!\n")
            return 1
        elif guess < secret:
            print("Too low.\n")
        else:
            print("Too high.\n")

    print(f"❌ Out of attempts. The number was {secret}.\n")
    return 0

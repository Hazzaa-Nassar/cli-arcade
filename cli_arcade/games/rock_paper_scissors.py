from __future__ import annotations
import random

CHOICES = ("rock", "paper", "scissors")

def _beats(a: str, b: str) -> bool:
    return (a == "rock" and b == "scissors") or (a == "paper" and b == "rock") or (a == "scissors" and b == "paper")

def play_rps() -> int:
    print("\n🎮 Rock Paper Scissors")
    print("Type: rock / paper / scissors (or q to quit)\n")

    user = input("Your choice: ").strip().lower()
    if user == "q":
        print("Bye!\n")
        return 0
    if user not in CHOICES:
        print("Invalid choice.\n")
        return 0

    cpu = random.choice(CHOICES)
    print(f"Computer chose: {cpu}")

    if user == cpu:
        print("🤝 Draw.\n")
        return -1
    if _beats(user, cpu):
        print("✅ You win!\n")
        return 1

    print("❌ You lose.\n")
    return 0

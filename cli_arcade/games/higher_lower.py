from __future__ import annotations
import random

def play_higher_lower() -> int:
    """
    Returns:
      1 -> win (7+ correct)
      0 -> loss/quit
    """
    print("\n🎮 Higher / Lower")
    print("Guess if the next number will be higher or lower.")
    print("Type: h = higher, l = lower, q = quit\n")

    rounds = 10
    needed = 7
    score = 0

    current = random.randint(1, 100)
    print(f"Start number: {current}\n")

    for r in range(1, rounds + 1):
        choice = input(f"Round {r}/{rounds} (h/l/q): ").strip().lower()
        if choice == "q":
            print("Bye!\n")
            return 0
        if choice not in ("h", "l"):
            print("Invalid. Use h, l, or q.\n")
            continue

        nxt = random.randint(1, 100)
        while nxt == current:
            nxt = random.randint(1, 100)

        correct = (choice == "h" and nxt > current) or (choice == "l" and nxt < current)

        print(f"Next number: {nxt}")
        if correct:
            score += 1
            print(f"✅ Correct!  (score={score})\n")
        else:
            print(f"❌ Wrong.    (score={score})\n")

        current = nxt

    print(f"Final score: {score}/{rounds}")
    if score >= needed:
        print("🏆 You win!\n")
        return 1

    print("Try again!\n")
    return 0

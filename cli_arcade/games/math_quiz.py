from __future__ import annotations
import random

def play_math_quiz() -> int:
    print("\n🎮 Math Quiz")
    print("Answer 5 questions. Get 4+ correct to win.\n")

    correct = 0
    total = 5

    for i in range(1, total + 1):
        a = random.randint(1, 12)
        b = random.randint(1, 12)
        op = random.choice(["+", "-", "*"])

        if op == "+":
            ans = a + b
        elif op == "-":
            ans = a - b
        else:
            ans = a * b

        raw = input(f"Q{i}/{total}: {a} {op} {b} = ").strip()
        if raw.lower() == "q":
            print("Quit.\n")
            return 0
        if not raw.lstrip("-").isdigit():
            print("Invalid input.\n")
            continue

        if int(raw) == ans:
            correct += 1
            print("✅ Correct\n")
        else:
            print(f"❌ Wrong (answer: {ans})\n")

    print(f"Score: {correct}/{total}\n")
    if correct >= 4:
        print("🏆 You win!\n")
        return 1

    print("Try again!\n")
    return 0

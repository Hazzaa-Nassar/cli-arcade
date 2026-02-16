from __future__ import annotations
import random
import time

PROMPTS = [
    "the quick brown fox jumps over the lazy dog",
    "practice makes progress and progress makes confidence",
    "write code as if the next person to maintain it is a tired you",
    "small steps every day beat big steps once a month",
    "focus on clarity first then optimize when it matters",
    "bugs hide in assumptions so test the edges and the weird cases",
    "ship something simple then improve it with real feedback",
    "keep functions short and names clear and everything gets easier",
    "your tools should work for you not the other way around",
    "consistency beats motivation when motivation disappears",
]

def _accuracy(target: str, typed: str) -> float:
    # character-level accuracy (includes spaces)
    if not target:
        return 0.0
    correct = 0
    for i, ch in enumerate(target):
        if i < len(typed) and typed[i] == ch:
            correct += 1
    return 100.0 * correct / len(target)

def _wpm(typed: str, seconds: float) -> float:
    # standard typing formula: 5 chars = 1 word
    if seconds <= 0:
        return 0.0
    words = len(typed) / 5.0
    return words * (60.0 / seconds)

def play_typing_test() -> int:
    """
    Win condition:
      WPM >= 30 AND accuracy >= 90%
    Returns:
      1 -> win
      0 -> loss/quit
    """
    prompt = random.choice(PROMPTS)

    print("\n🎮 Typing Test")
    print("Type the sentence exactly as shown.")
    print("Press Enter to start. Type 'q' then Enter to quit.\n")
    print(f"Prompt:\n{prompt}\n")

    start_cmd = input("Ready? (Enter to start): ").strip().lower()
    if start_cmd == "q":
        print("Bye!\n")
        return 0

    print("\nGo!\n")
    t0 = time.perf_counter()
    typed = input("> ")
    t1 = time.perf_counter()

    if typed.strip().lower() == "q":
        print("Bye!\n")
        return 0

    elapsed = t1 - t0
    acc = _accuracy(prompt, typed)
    wpm = _wpm(typed, elapsed)

    print("\n--- Results ---")
    print(f"Time: {elapsed:.2f}s")
    print(f"WPM:  {wpm:.1f}")
    print(f"Acc:  {acc:.1f}%\n")

    if wpm >= 30.0 and acc >= 90.0:
        print("✅ You win! Nice typing.\n")
        return 1

    print("❌ Not quite. Try again!\n")
    return 0

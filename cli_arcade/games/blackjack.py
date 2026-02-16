from __future__ import annotations
import random

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUITS = ["♠", "♥", "♦", "♣"]

def _draw_card() -> str:
    # infinite-deck style: random cards, no counting
    return f"{random.choice(RANKS)}{random.choice(SUITS)}"

def _rank(card: str) -> str:
    # "10♣" -> "10", "A♦" -> "A"
    return card[:-1]

def _hand_value(cards: list[str]) -> int:
    ranks = [_rank(c) for c in cards]
    total = 0
    aces = 0

    for r in ranks:
        if r == "A":
            aces += 1
            total += 11
        elif r in ("K", "Q", "J"):
            total += 10
        else:
            total += int(r)

    # downgrade aces from 11 -> 1 while busting
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total

def _is_blackjack(cards: list[str]) -> bool:
    return len(cards) == 2 and _hand_value(cards) == 21

def _show_hand(name: str, cards: list[str], hide_first: bool = False) -> None:
    if hide_first:
        shown = ["??"] + cards[1:]
        print(f"{name}: {' '.join(shown)}")
    else:
        print(f"{name}: {' '.join(cards)}  (value={_hand_value(cards)})")

def play_blackjack() -> int:
    """
    Returns:
      1  -> win
      0  -> loss/quit
     -1  -> draw (push)
    """
    print("\n🎮 Blackjack")
    print("Rules: dealer stands on 17+. Aces are 1 or 11. Type h=hit, s=stand, q=quit.\n")

    player = [_draw_card(), _draw_card()]
    dealer = [_draw_card(), _draw_card()]

    _show_hand("Dealer", dealer, hide_first=True)
    _show_hand("You", player)

    # naturals
    p_bj = _is_blackjack(player)
    d_bj = _is_blackjack(dealer)
    if p_bj or d_bj:
        _show_hand("Dealer", dealer, hide_first=False)
        if p_bj and d_bj:
            print("🤝 Both blackjack. Push.\n")
            return -1
        if p_bj:
            print("✅ Blackjack! You win!\n")
            return 1
        print("❌ Dealer blackjack. You lose.\n")
        return 0

    # player turn
    while True:
        pv = _hand_value(player)
        if pv > 21:
            print("❌ Bust. You lose.\n")
            return 0

        choice = input("Your move (h/s/q): ").strip().lower()
        if choice == "q":
            print("Bye!\n")
            return 0
        if choice == "h":
            player.append(_draw_card())
            _show_hand("You", player)
            continue
        if choice == "s":
            break
        print("Invalid. Type h, s, or q.\n")

    # dealer turn
    _show_hand("Dealer", dealer, hide_first=False)
    while _hand_value(dealer) < 17:
        dealer.append(_draw_card())
        _show_hand("Dealer", dealer, hide_first=False)

    dv = _hand_value(dealer)
    pv = _hand_value(player)

    if dv > 21:
        print("✅ Dealer busts. You win!\n")
        return 1
    if pv > dv:
        print("✅ You win!\n")
        return 1
    if pv < dv:
        print("❌ You lose.\n")
        return 0

    print("🤝 Push (draw).\n")
    return -1

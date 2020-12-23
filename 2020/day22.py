import sys

def main():
    lines = [line.rstrip() for line in sys.stdin]
    deck1, deck2 = parse_lines(lines)

    # Part 1
    while deck1 and deck2:
        c1, c2 = deck1.pop(0), deck2.pop(0)
        if c1 > c2:
            deck1 += [c1, c2]
        else:
            deck2 += [c2, c1]
    deck_win = deck1 or deck2
    print("Score:", score(deck_win))

    # Part 2
    deck1, deck2 = parse_lines(lines)
    winner = rec_game(deck1, deck2)
    deck_win = deck1 if winner == 1 else deck2
    print("Score:", score(deck_win))

def parse_lines(lines):
    deck1, deck2 = [], []
    for line in lines:
        if not line:
            continue
        if line.startswith("P"):
            deck = deck1 if int(line[7:8]) == 1 else deck2
        else:
            deck.append(int(line))
    return deck1, deck2

def score(deck):
    return sum(c * (i + 1) for i, c in enumerate(reversed(deck)))

def rec_game(deck1, deck2):
    past_decks = set()
    while deck1 and deck2:
        h = tuple(deck1), tuple(deck2)
        if h in past_decks:
            return 1
        past_decks.add(h)
        c1, c2 = deck1.pop(0), deck2.pop(0)
        if len(deck1) >= c1 and len(deck2) >= c2:
            if rec_game(deck1[:c1], deck2[:c2]) == 1:
                deck1 += [c1, c2]
            else:
                deck2 += [c2, c1]
        elif c1 > c2:
            deck1 += [c1, c2]
        else:
            deck2 += [c2, c1]
    return 1 if deck1 else 2

if __name__ == "__main__":
    main()

EX1 = [
    "cut 6",
    "deal with increment 7",
    "deal into new stack",
]


def main():
    with open("day22.txt") as input_file:
        lines = [l.rstrip() for l in input_file.readlines()]

    deck = list(range(10007))
    for line in lines:
        # Deal into new stack.
        if line.endswith("k"):
            deck.reverse()
            continue

        arg = int(line[line.rfind(" "):])

        # Deal with increment.
        if line[0] == "d":
            new_deck = [None] * len(deck)
            for i in range(len(deck)):
                new_deck[(i * arg) % len(new_deck)] = deck[i]
            deck = new_deck

        # Cut.
        elif line[0] == "c":
            cut, deck = deck[:arg], deck[arg:]
            deck += cut

    print(f"Position of card 2019: {deck.index(2019)}.")


if __name__ == "__main__":
    main()

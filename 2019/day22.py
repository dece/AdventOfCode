EX1 = [
    "deal with increment 7",
    "deal into new stack",
    "deal into new stack",
]
EX2 = [
    "cut 6",
    "deal with increment 7",
    "deal into new stack",
]
EX3 = [
    "deal with increment 7",
    "deal with increment 9",
    "cut -2",
]
EX4 = [
    "deal into new stack",
    "cut -2",
    "deal with increment 7",
    "cut 8",
    "cut -4",
    "deal with increment 7",
    "cut 3",
    "deal with increment 9",
    "deal with increment 3",
    "cut -1",
]

def main():
    with open("day22.txt") as input_file:
        lines = [l.rstrip() for l in input_file.readlines()]

    # Part 1
    deck = list(range(10))
    # deck = list(range(10007))
    deck = part1(deck, EX3)
    print(deck)
    # deck = part1(deck, lines)
    # print(f"Position of card 2019: {deck.index(2019)}.")

    # Part 2
    part2(10, 1, EX3, pos=0); input()
    part2(10, 1, EX3, pos=1); input()
    part2(10, 1, EX3, pos=2); input()
    part2(10, 1, EX3, pos=3); input()
    part2(10, 1, EX3, pos=4); input()
    part2(10, 1, EX3, pos=5); input()
    part2(10, 1, EX3, pos=6); input()
    part2(10, 1, EX3, pos=7); input()
    part2(10, 1, EX3, pos=8); input()
    part2(10, 1, EX3, pos=9); input()
    # part2(10007, 1, lines, pos=8191)
    # part2(119315717514047, 101741582076661, lines)
    # print(f"2020th card: {deck[2020]}.")

def part1(deck, commands):
    for command in commands:
        # Deal into new stack.
        if command.endswith("k"):
            deck.reverse()
            continue
        arg = int(command[command.rfind(" "):])
        # Deal with increment.
        if command[0] == "d":
            new_deck = [None] * len(deck)
            for i in range(len(deck)):
                new_deck[(i * arg) % len(new_deck)] = deck[i]
            deck = new_deck
        # Cut.
        elif command[0] == "c":
            cut, deck = deck[:arg], deck[arg:]
            deck += cut
    return deck

def part2(deck_len, num_shuf, commands, pos=2020):
    required = find_required(deck_len, commands, pos)
    for c, r in zip(commands, required):
        print(f"- Command '{c}' requires knowing value at {r[0]} for {r[1]}.")
    print(f"Which gives us value at {pos}.")
    deck = {i: i for r in required for i in r}
    print(required)
    print("Shuffling...")
    shuffle(deck, required)
    print(f"Card at {pos}: {deck[pos]}.")

def find_required(deck_len, commands, pos):
    required = []
    for command in reversed(commands):
        dest = pos
        if command.endswith("k"):
            pos = req_dins(pos, deck_len)
            required.append((pos, dest))
            continue
        arg = int(command[command.rfind(" "):])
        if command[0] == "d":
            print(f"What's req for {pos} in deal with increment {arg}?")
            pos = req_dwi(pos, deck_len, arg)
            print(f"- answer: {pos}.")
        elif command[0] == "c":
            pos = req_cut(pos, deck_len, arg)
        required.append((pos, dest))
    required.reverse()
    return required

def req_dins(pos, deck_len):
    return deck_len - 1 - pos

def req_cut(pos, deck_len, n):
    return (pos + n) % deck_len

def req_dwi(pos, deck_len, inc):
    # Straight is (i * arg) % deck_len = j
    # (i * arg) = modinv(j, deck_len)
    # i = modinv(j, deck_len) / arg
    # damn idk
    return (pos * inc - deck_len) % deck_len

def shuffle(deck, required):
    for required_pair in required:
        from_pos, to_pos = required_pair
        deck[to_pos] = deck[from_pos]

def dins(parameter_list):
    pass

def cut(parameter_list):
    pass

def dwi(parameter_list):
    pass


if __name__ == "__main__":
    # main()

    assert req_cut(0, 10, 3) == 3
    assert req_cut(1, 10, 3) == 4
    assert req_cut(2, 10, 3) == 5
    assert req_cut(5, 10, 3) == 8
    assert req_cut(8, 10, 3) == 1
    assert req_cut(0, 10, -4) == 6
    assert req_cut(0, 10, -4) == 6
    assert req_cut(1, 10, -4) == 7
    assert req_cut(2, 10, -4) == 8
    assert req_cut(3, 10, -4) == 9
    assert req_cut(4, 10, -4) == 0
    assert req_cut(5, 10, -4) == 1
    assert req_cut(6, 10, -4) == 2
    assert req_cut(7, 10, -4) == 3
    assert req_cut(8, 10, -4) == 4
    assert req_cut(9, 10, -4) == 5

    assert req_dins(0, 10) == 9
    assert req_dins(1, 10) == 8
    assert req_dins(2, 10) == 7
    assert req_dins(8, 10) == 1
    assert req_dins(9, 10) == 0

    assert req_dwi(0, 10, 3) == 0
    assert req_dwi(1, 10, 3) == 7
    assert req_dwi(2, 10, 3) == 4
    assert req_dwi(3, 10, 3) == 1
    assert req_dwi(4, 10, 3) == 8
    assert req_dwi(5, 10, 3) == 5
    assert req_dwi(6, 10, 3) == 2
    assert req_dwi(7, 10, 3) == 9
    assert req_dwi(8, 10, 3) == 6
    assert req_dwi(9, 10, 3) == 3

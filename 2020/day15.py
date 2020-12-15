import sys
from collections import defaultdict


def main():
    nl = list(map(lambda s: int(s), sys.stdin.read().rstrip().split(",")))

    # Part 1
    print("Part 1:", get_nth(2020, nl))
    # Part 2
    print("Part 2:", get_nth(30000000, nl))


def get_nth(limit, starters):  # pretty horrible complexity but i'm behind sched
    said = defaultdict(list)
    for turn in range(1, limit + 1):
        if turn <= len(starters):  # starting number shit special case.
            n = starters[turn - 1]
        else:
            last_spoken = n
            if len(said[last_spoken]) == 1:
                n = 0
            else:
                last_turn_said = said[last_spoken][-2]
                n = turn - 1 - last_turn_said
        said[n].append(turn)
        said[n] = said[n][-2:]
    return n


if __name__ == "__main__":
    main()

import math
import sys
from functools import reduce
from itertools import combinations


def main():
    lines = [line.rstrip() for line in sys.stdin]
    earliest = int(lines[0])
    ids = map(int, filter(lambda s: s != "x", lines[1].split(",")))

    # Part 1
    wait_times = {i: i - (earliest % i) for i in ids}
    best_id, wait = min(wait_times.items(), key=lambda item: item[1])
    print("Part 1:", best_id * wait)

    # Part 2
    # math shit
    # https://en.wikipedia.org/wiki/Chinese_remainder_theorem wtf is going on
    ids = []
    rems = []
    for i, v in enumerate(lines[1].split(",")):
        if v != "x":
            # import hint: you want to use negative indices for remainders to
            # use it with CRT here.
            rems.append(-i)
            ids.append(int(v))
    # are all bus IDs co-prime?
    assert all(math.gcd(a, b) == 1 for a, b in combinations(ids, 2))
    # CRT
    # https://www.youtube.com/watch?v=zIFehsBHB8o
    N = reduce(lambda a, b: a * b, ids, 1)
    x = 0
    for ni, ai in zip(ids, rems):
        Ni = N // ni
        x += ai * Ni * pow(Ni, -1, ni)
    x %= N
    print("Part 2:", x)


if __name__ == "__main__":
    main()

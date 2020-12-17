import sys
from itertools import product


def main():
    lines = [line.rstrip() for line in sys.stdin]

    print("Actives:", solve(lines, 3))
    print("Hyperactives:", solve(lines, 4))


def solve(lines, dimensions):
    s = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            p = (x, y) + (0,) * (dimensions - 2)
            s[p] = 1 if c == "#" else 0
    for _ in range(6):
        cycle(s)
    return sum(s.values())


def cycle(s):
    future = {}
    work_set = set(nn for pos in s for nn in near(*pos))
    for pos in work_set:
        an = 0
        for nn in near(*pos):
            an += s.get(nn, 0)
        if (v := s.get(pos, 0)) == 1 and not 2 <= an <= 3:
            future[pos] = 0
        elif v == 0 and an == 3:
            future[pos] = 1
    for f, fv in future.items():
        s[f] = fv


def near(*comp):
    num_comp = len(comp)
    offsets = list(product([-1, 0, 1], repeat=num_comp))
    offsets.remove((0,) * num_comp)
    for p in offsets:
        yield tuple(c + o for c, o in zip(comp, p))


if __name__ == "__main__":
    main()

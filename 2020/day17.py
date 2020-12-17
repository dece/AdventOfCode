import sys


def main():
    lines = [line.rstrip() for line in sys.stdin]; sys.stdin = open("/dev/tty")

    print("Actives:", part1(lines))
    print("Hyperactives:", part2(lines))


def part1(lines):
    s = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            s[(x, y, 0)] = 1 if c == "#" else 0
    for _ in range(6):
        cycle(s)
    return sum(s.values())


def cycle(s):
    future = {}
    work_set = set(nn for x, y, z in s for nn in near(x, y, z))
    for x, y, z in work_set:
        an = 0
        for nn in near(x, y, z):
            an += s.get(nn, 0)
        if (v := s.get((x, y, z), 0)) == 1 and not 2 <= an <= 3:
            future[(x, y, z)] = 0
        elif v == 0 and an == 3:
            future[(x, y, z)] = 1
    for f, fv in future.items():
        s[f] = fv


def near(x, y, z, include_self=False):
    for zi in range(-1, 2):
        for yi in range(-1, 2):
            for xi in range(-1, 2):
                if include_self or xi != 0 or yi != 0 or zi != 0:
                    yield x + xi, y + yi, z + zi


def part2(lines):
    h = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            h[(x, y, 0, 0)] = 1 if c == "#" else 0
    for _ in range(6):
        cycle2(h)
    return sum(h.values())


def cycle2(h):
    future = {}
    work_set = set(nn for x, y, z, w in h for nn in hyper_near(x, y, z, w))
    for x, y, z, w in work_set:
        an = 0
        for nn in hyper_near(x, y, z, w):
            an += h.get(nn, 0)
        if (v := h.get((x, y, z, w), 0)) == 1 and not 2 <= an <= 3:
            future[(x, y, z, w)] = 0
        elif v == 0 and an == 3:
            future[(x, y, z, w)] = 1
    for f, fv in future.items():
        h[f] = fv


def hyper_near(x, y, z, w, include_self=False):  # oh boy
    for wi in range(-1, 2):
        for zi in range(-1, 2):
            for yi in range(-1, 2):
                for xi in range(-1, 2):
                    if include_self or xi != 0 or yi != 0 or zi != 0 or wi != 0:
                        yield x + xi, y + yi, z + zi, w + wi


if __name__ == "__main__":
    main()

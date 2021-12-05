import sys
from collections import defaultdict


def main():
    lines = [line.rstrip() for line in sys.stdin]
    coords = [
        tuple(map(
            lambda s: tuple(map(int, s.split(","))),
            line.split(" -> ")
        ))
        for line in lines
    ]

    # Part 1
    data = defaultdict(int)
    for (x1, y1), (x2, y2) in coords:
        if x1 == x2:
            ymin, ymax = min(y1, y2), max(y1, y2)
            for y in range(ymin, ymax + 1):
                data[(x1, y)] += 1
        elif y1 == y2:
            xmin, xmax = min(x1, x2), max(x1, x2)
            for x in range(xmin, xmax + 1):
                data[(x, y1)] += 1
    print(sum(v > 1 for v in data.values()))

    # Part 2 - reuse previous data and just consider diagonals
    for (x1, y1), (x2, y2) in coords:
        if x1 != x2 and y1 != y2:
            xofs = 1 if x1 < x2 else -1
            yofs = 1 if y1 < y2 else -1
            while True:
                data[(x1, y1)] += 1
                if x1 == x2:
                    break
                x1 += xofs
                y1 += yofs
    print(sum(v > 1 for v in data.values()))


if __name__ == "__main__":
    main()

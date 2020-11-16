import re

from grid import Grid


EX = [
    "#1 @ 1,3: 4x4",
    "#2 @ 3,1: 4x4",
    "#3 @ 5,5: 2x2",
]


def main():
    with open("day3.txt", "rt") as f:
        lines = [line.rstrip() for line in f.readlines()]

    # Part 1
    g = Grid()
    for line in lines:
        ident, left, top, width, height = parse_line(line)
        for i in range(int(width)):
            for j in range(int(height)):
                x = int(left) + i
                y = int(top) + j
                g.setv(x, y, g.getv(x, y) + 1)
    n = get_overlaps(g)
    print(n)

    # Part 2
    g = Grid()
    over = []
    for line in lines:
        ident, left, top, width, height = parse_line(line)
        for i in range(int(width)):
            for j in range(int(height)):
                x = int(left) + i
                y = int(top) + j
                current_v = g.getv(x, y)
                if current_v == None:
                    over.append(int(ident))
                    continue
                elif current_v == 0:
                    g.setv(x, y, int(ident))
                else:
                    over += [int(ident), current_v]
                    g.setv(x, y, None)
    print(set(v for _, _, v in g.values_gen()).difference(set(over)))

LINE_RE = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")

def parse_line(line):
    match = LINE_RE.match(line)
    return match.groups()

def get_overlaps(grid):
    return sum([v > 1 for _, _, v in grid.values_gen()])

if __name__ == "__main__":
    main()

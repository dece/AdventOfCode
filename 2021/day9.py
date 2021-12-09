import sys


def main():
    lines = [line.rstrip() for line in sys.stdin]
    nc = len(lines[0])
    nr = len(lines)
    m = [list(map(int, line)) for line in lines]

    # Part 1
    low_points = []
    rlevels = 0
    for x, row in enumerate(m):
        for y, val in enumerate(row):
            if (
                (x == 0 or m[x - 1][y] > val)
                and (x == nr - 1 or m[x + 1][y] > val)
                and (y == 0 or m[x][y - 1] > val)
                and (y == nc - 1 or m[x][y + 1] > val)
            ):
                low_points.append((x, y))  # for part 2
                rlevels += val + 1
    print(rlevels)

    # Part 2
    basins = [expand_basin(m, (x, y), nc, nr) for x, y in low_points]
    a, b, c = sorted(map(len, basins))[-3:]
    print(a * b * c)


def expand_basin(m, start, nc, nr):
    basin = []
    sx, sy = start
    explo = [(sx, sy)]
    while explo:
        pos = explo.pop(0)
        x, y = pos
        if m[x][y] == 9:
            continue
        basin.append(pos)
        if x > 0 and (n := (x - 1, y)) not in basin and n not in explo:
            explo.append(n)
        if x < nr - 1 and (n := (x + 1, y)) not in basin and n not in explo:
            explo.append(n)
        if y > 0 and (n := (x, y - 1)) not in basin and n not in explo:
            explo.append(n)
        if y < nc - 1 and (n := (x, y + 1)) not in basin and n not in explo:
            explo.append(n)
    return basin


if __name__ == "__main__":
    main()

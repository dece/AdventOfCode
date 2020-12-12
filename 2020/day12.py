import sys


def main():
    codes = [(line[0], int(line.rstrip()[1:])) for line in sys.stdin]

    # Part 1
    x, y = 0, 0
    dofs = [(1, 0), (0, -1), (-1, 0), (0, 1)]  # E S W N
    dmap = {di: do for di, do in zip("ESWN", dofs)}
    f = 0
    for ci, cv in codes:
        if (dd := dmap.get(ci)):
            dx, dy = dd
            x, y = x + dx * cv, y + dy * cv
        elif ci in "LR":
            r = cv // 90
            f = (f - r if ci == "L" else f + r) % 4
        else:  # F
            dx, dy = dofs[f]
            x, y = x + dx * cv, y + dy * cv
    print("Manhattan distance:", abs(x) + abs(y))

    # Part 2
    x, y = 0, 0
    wx, wy = 10, 1
    for ci, cv in codes:
        if (dd := dmap.get(ci)):
            dx, dy = dd
            wx, wy = wx + dx * cv, wy + dy * cv
        elif ci in "LR":  # what are matrices
            dx, dy = wx - x, wy - y
            if (ci, cv) in (("R", 90), ("L", 270)):
                wx, wy = x + dy, y - dx
            elif (ci, cv) in (("R", 270), ("L", 90)):
                wx, wy = x - dy, y + dx
            else:  # 180°
                wx, wy = x - dx, y - dy
        else:  # F
            dx, dy = wx - x, wy - y
            x, y = x + dx * cv, y + dy * cv
            wx, wy = x + dx, y + dy
    print("Manhattan distance part 2:", abs(x) + abs(y))


if __name__ == "__main__":
    main()

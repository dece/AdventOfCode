from grid import Grid


def main():
    with open("day3.txt", "rt") as f:
        lines = [line.rstrip() for line in f.readlines()]
    g = Grid(lambda: ".")
    g.load(lines)
    g_width = len(lines[0])
    g_height = len(lines)

    # Part 1
    x, y = 0, 0
    num_trees = 0
    while y < g_height:
        x += 3
        x %= g_width
        y += 1
        if g.getv(x, y) == "#":
            num_trees += 1
    print("Trees encountered:", num_trees)

    # Part 2
    v = 1
    for xx, yy in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        x, y = 0, 0
        num_trees = 0
        while y < g_height:
            x += xx
            x %= g_width
            y += yy
            if g.getv(x, y) == "#":
                num_trees += 1
        print(f"Slope ({xx}, {yy}), trees encountered:", num_trees)
        v *= num_trees
    print("Value:", v)


if __name__ == "__main__":
    main()

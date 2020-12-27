import sys

from grid import Grid

def main():
    lines = [line.rstrip() for line in sys.stdin]
    g = Grid(value_factory=int)

    # Part 1
    for line in lines:
        x, y = 0, 0
        while line:
            if line[0] in ("e", "w"):
                x, y = move(x, y, line[0])
                line = line[1:]
            else:
                x, y = move(x, y, line[:2])
                line = line[2:]
        g.setv(x, y, abs(g.getv(x, y) - 1))
    print("Black tiles:", sum(v for _, _, v in g.values_gen()))

    # Part 2 aka stop using this grid class it's horrible
    for _ in range(100):
        expand(g)
        yagol(g)
    print("Black tiles p2:", sum(v for _, _, v in g.values_gen()))

def move(x, y, d):
    if d in ("e", "w"):
        x += 1 if d == "e" else -1
    else:
        dy, dx = d[0], d[1]
        if y % 2 == 0 and dx == "w":
            x -= 1
        elif y % 2 == 1 and dx == "e":
            x += 1
        y += 1 if dy == "s" else -1
    return x, y

D = ["e", "se", "sw", "w", "nw", "ne"]

def expand(g):
    for x, y, _ in list(g.values_gen()):
        for d in D:
            dx, dy = move(x, y, d)
            if not g.hasv(dx, dy):
                g.setv(dx, dy, 0)

def yagol(g):
    c = {}
    for x, y, v in g.values_gen():
        bn = 0
        for d in D:
            nx, ny = move(x, y, d)
            if g.hasv(nx, ny):
                bn += g.getv(nx, ny)
        if v == 1 and (bn == 0 or bn > 2):
            c[(x, y)] = 0
        elif v == 0 and bn == 2:
            c[(x, y)] = 1
    for (x, y), v in c.items():
        g.setv(x, y, v)

if __name__ == "__main__":
    main()

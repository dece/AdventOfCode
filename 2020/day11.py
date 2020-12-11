import sys

from grid import Grid, near8


def main():
    lines = [line.rstrip() for line in sys.stdin]

    # Part 1
    g = Grid(value_factory=lambda: ".", lines=lines)
    while update(g):
        pass
    print("Occupied:", sum(v == "#" for _, _, v in g.values_gen()))

    # Part 2
    g = Grid(value_factory=lambda: ".", lines=lines)
    while update2(g):
        pass
    print("Occupied part 2:", sum(v == "#" for _, _, v in g.values_gen()))


def update(g):
    changes = {}
    for x, y, v in g.values_gen():
        if v == ".":
            continue
        p = (x, y)
        n = list(g.near_objects(p, near_f=near8).values())
        if v == "L" and n.count("#") == 0:
            changes[p] = "#"
        elif v == "#" and n.count("#") >= 4:
            changes[p] = "L"
    for (x, y), v in changes.items():
        g.setv(x, y, v)
    return bool(changes)


RAYS_OFS = [
    (-1, -1), ( 0, -1), ( 1, -1),
    (-1,  0),           ( 1,  0),
    (-1,  1), ( 0,  1), ( 1,  1),
]


def update2(g):
    changes = {}
    for x, y, v in g.values_gen():
        if v == ".":
            continue
        occ = 0 
        for ox, oy in RAYS_OFS:
            n = 1
            while True:
                qx, qy = x + ox * n, y + oy * n
                if not g.hasv(qx, qy):
                    break
                if (rv := g.getv(qx, qy)) == "#":
                    occ += 1
                    break
                elif rv == "L":
                    break
                n += 1
        if v == "L" and occ == 0:
            changes[(x, y)] = "#"
        elif v == "#" and occ >= 5:
            changes[(x, y)] = "L"
    for (x, y), v in changes.items():
        g.setv(x, y, v)
    return bool(changes)


if __name__ == "__main__":
    main()

"""Generic 2D grid with a few helpers."""

from collections import defaultdict


def near(p):
    """Return a tuple of neighbor positions (up, left, down, right)."""
    return (
        (p[0]    , p[1] - 1),
        (p[0] + 1, p[1]    ),
        (p[0]    , p[1] + 1),
        (p[0] - 1, p[1]    ),
    )


def near8(p):
    """Return a tuple of neighbor positions, including diagonals."""
    return (
        (p[0] - 1, p[1] - 1),
        (p[0]    , p[1] - 1),
        (p[0] + 1, p[1] - 1),
        (p[0] - 1, p[1]    ),
        (p[0] + 1, p[1]    ),
        (p[0] - 1, p[1] + 1),
        (p[0]    , p[1] + 1),
        (p[0] + 1, p[1] + 1),
    )


class Grid:

    def __init__(self, value_factory=int, lines=None):
        self.g = defaultdict(lambda: defaultdict(value_factory))
        if lines:
            self.load(lines)

    def hasv(self, x, y):
        return y in self.g and x in self.g[y]

    def getv(self, x, y):
        return self.g[y][x]

    def setv(self, x, y, value):
        self.g[y][x] = value

    def load(self, lines, f=lambda v: v):
        for y, line in enumerate(lines):
            for x, c in enumerate(line.rstrip()):
                self.g[y][x] = f(c)

    def values_gen(self):
        for y, row in self.g.items():
            for x, v in row.items():
                yield (x, y, v)

    def near_objects(self, p, near_f=near):
        return {
            q: self.getv(q[0], q[1])
            for q in near_f(p)
            if self.hasv(q[0], q[1])  # do not create entries.
        }

    def dumb_print(self, f=lambda v: v):
        for row in self.g.values():
            for x in row.values():
                print(f(x), end="")
            print()

    def print_near(self, p, view_size=2):
        for dy in range(-view_size, view_size + 1):
            print("".join([
                self.g[p[1] + dy][p[0] + dx]
                for dx in range(-view_size, view_size + 1)
            ]))

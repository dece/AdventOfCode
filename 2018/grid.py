"""Generic 2D grid with a few helpers."""

from collections import defaultdict


class Grid:

    def __init__(self, value_factory=int, lines=None):
        self.g = defaultdict(lambda: defaultdict(value_factory))
        if lines:
            self.load(lines)

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

    def near_objects(self, p):
        """Return a dict of neighbor positions to values (U, L, D, R)."""
        return {q: self.g[q[1]][q[0]] for q in Grid.near(p)}

    def dumb_print(self, f=lambda v: v):
        for row in self.g.values():
            for x in row.values():
                print(f(x), end="")
            print()

    def print_near(self, p, view_size=2):
        """Print near values in an area of view_size. Works iff keys support addition."""
        for dy in range(-view_size, view_size + 1):
            print("".join([
                self.g[p[1] + dy][p[0] + dx]
                for dx in range(-view_size, view_size + 1)
            ]))

    @staticmethod
    def near(p):
        """Return a tuple of neighbor positions (up, left, down, right)."""
        return (
            (p[0]    , p[1] - 1),
            (p[0] + 1, p[1]    ),
            (p[0]    , p[1] + 1),
            (p[0] - 1, p[1]    ),
        )

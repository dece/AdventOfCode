"""Generic 2D grid with a few helpers."""

from collections import defaultdict


class Grid:

    def __init__(self, lines=None):
        self.g = defaultdict(lambda: defaultdict(int))
        if lines:
            self.load(lines)

    def load(self, lines, f=lambda v: v):
        for y, line in enumerate(lines):
            for x, c in enumerate(line.rstrip()):
                self.g[y][x] = f(c)

    def getv(self, x, y):
        return self.g[y][x]
    
    def setv(self, x, y, value):
        self.g[y][x] = value

    def near_items(self, p):
        """Return a dict of neighbor positions to values (U, L, D, R)."""
        return {pos: self.g[pos[1]][pos[0]] for pos in Grid.near(p)}

    def dumb_print(self, f=lambda v: v):
        for row in self.g.values():
            for x in row.values():
                print(f(x), end="")
            print()

    def print_near(self, p):
        print("".join([
            chr(self.g[p[1] - 1][p[0] - 1]),
            chr(self.g[p[1] - 1][p[0]]),
            chr(self.g[p[1] - 1][p[0] + 1]),
        ]))
        print("".join([
            chr(self.g[p[1]    ][p[0] - 1]),
            chr(self.g[p[1]    ][p[0]]),
            chr(self.g[p[1]    ][p[0] + 1]),
        ]))
        print("".join([
            chr(self.g[p[1] + 1][p[0] - 1]),
            chr(self.g[p[1] + 1][p[0]]),
            chr(self.g[p[1] + 1][p[0] + 1]),
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

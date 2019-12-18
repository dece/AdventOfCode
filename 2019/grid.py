from collections import defaultdict


class Grid:

    def __init__(self):
        self.g = defaultdict(lambda: defaultdict(int))

    @staticmethod
    def near(p):
        """Return a tuple of neighbor positions (up, left, down, right)."""
        return (
            (p[0]    , p[1] - 1),
            (p[0] + 1, p[1]    ),
            (p[0]    , p[1] + 1),
            (p[0] - 1, p[1]    ),
        )

    def near_items(self, p):
        """Return a dict of neighbor positions to values (U, L, D, R)."""
        return {pos: self.g[pos[1]][pos[0]] for pos in Grid.near(p)}

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

from collections import defaultdict


class Grid:

    def __init__(self):
        self.g = defaultdict(lambda: defaultdict(int))

    def values(self):
        for a, chunk in self.g.items():
            for b, v in chunk.items():
                yield a, b, v

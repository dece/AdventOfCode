import string

from grid import Grid
from vector import v2a


EX1 = [
    "#########",
    "#b.A.@.a#",
    "#########",
]
# reqs: 
# a: []
# b: [a]
EX2 = [
    "########################",
    "#f.D.E.e.C.b.A.@.a.B.c.#",
    "######################.#",
    "#d.....................#",
    "########################",
]
# reqs: 
# a: []
# b: [a]
# c: [b]
# d: [b]
# e: [a, c]
# f: [a, c, e, d]
# 
# - get a
# - get b
# - get c or d?
#   - get c
#     - get d or e?
#   - d


def main():
    with open("day18.txt", "rt") as input_file:
        lines = input_file.readlines()
    
    lab = Lab(lines=EX1)
    lab.dumb_print()

    lab.find_positions()
    pos = lab.start
    missing_keys = list(lab.key_pos.keys())
    obtained_keys = set("a")
    while missing_keys:

        for key, bt in lab.get_all_backtracks(pos).items():
            steps, reqs, founds = bt
            if len(reqs - obtained_keys) == 0:
                print(key, "is accessible")
        break


class Lab(Grid):

    TILE_PATH = "."
    TILE_WALL = "#"
    TILE_START = "@"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, value_factory=lambda: " ")
        self.start = None
        self.key_pos = {}
        self.door_pos = {}

    def find_positions(self):
        for x, y, v in self.values_gen():
            if v == Lab.TILE_START:
                self.start = (x, y)
            if v in string.ascii_lowercase:
                self.key_pos[v] = (x, y)
            if v in string.ascii_uppercase:
                self.door_pos[v] = (x, y)
        self.setv(self.start[0], self.start[1], Lab.TILE_PATH)
    
    def get_all_backtracks(self, start):
        return {
            kname: self.backtrack(self.path(start, kpos), kpos, start)
            for kname, kpos in self.key_pos.items()
        }

    def path(self, s, e):
        discovered = Grid(value_factory=bool)
        discovered.setv(s[0], s[1], True)
        parents = {}
        q = [s]
        while q:
            pos = q.pop(0)
            if pos == e:
                return parents
            nears = self.near_objects(pos)
            for near_pos, near_tile in nears.items():
                if near_tile == Lab.TILE_WALL:
                    continue
                if discovered.getv(near_pos[0], near_pos[1]):
                    continue
                discovered.setv(near_pos[0], near_pos[1], True)
                parents[near_pos] = pos
                q.append(near_pos)
        return parents

    def backtrack(self, parents, pos, end):
        count = 0
        requirements = set()
        keys_found = set()
        while pos != end:
            pos = parents[pos]
            count += 1
            tile = self.getv(pos[0], pos[1])
            if tile in string.ascii_uppercase:
                requirements.add(tile.lower())
            elif tile in string.ascii_lowercase:
                keys_found.add(tile)
        return count, requirements, keys_found


if __name__ == "__main__":
    main()

import string
import sys

from grid import Grid
from vector import v2a


EX1 = [
    "#########",
    "#b.A.@.a#",
    "#########",
]
EX2 = [
    "########################",
    "#f.D.E.e.C.b.A.@.a.B.c.#",
    "######################.#",
    "#d.....................#",
    "########################",
]


def main():
    with open("day18.txt", "rt") as input_file:
        lines = input_file.readlines()
    
    lab = Lab(lines=lines)
    lab.dumb_print()
    lab.find_positions()
    states = [(lab.start, frozenset(), 0)]
    state_cache = Grid(value_factory=dict)
    num_keys = len(lab.key_pos)
    min_steps = 2**32
    num_processed = 0
    while states:
        num_processed += 1
        pos, obtained, total_steps = states.pop(0)
        if len(obtained) == num_keys:
            print(f"All keys obtained in {total_steps}.")
            min_steps = min(min_steps, total_steps)
            continue

        for key_name, bt in lab.get_missing_backtracks(pos, keys=obtained).items():
            steps, required, found = bt
            if len(required - obtained) > 0:
                continue
            
            next_pos = lab.key_pos[key_name]
            next_obtained = obtained | found | {key_name}
            next_steps = total_steps + steps

            old_bests = state_cache.getv(next_pos[0], next_pos[1])
            if next_obtained not in old_bests or old_bests[next_obtained] > next_steps:
                print("o", end="")
                states.append((next_pos, next_obtained, next_steps))
                old_bests[next_obtained] = next_steps
            print(".", end="")

        if num_processed % 100 == 0:
            print(f"[{num_processed}/{len(states)}]", end="")
        sys.stdout.flush()
    print(f"Minimal number of steps to get all keys: {min_steps}.")

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
    
    def get_missing_backtracks(self, start, keys=set()):
        backtracks = {}
        for kname, kpos in self.key_pos.items():
            if kname in keys:
                continue
            path = self.path(start, kpos, keys=keys)
            if path is None:
                continue
            backtracks[kname] = self.backtrack(path, kpos, start)
        return backtracks

    def path(self, s, e, keys=set()):
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
                if near_tile in string.ascii_uppercase and near_tile.lower() not in keys:
                    continue
                if discovered.getv(near_pos[0], near_pos[1]):
                    continue
                discovered.setv(near_pos[0], near_pos[1], True)
                parents[near_pos] = pos
                q.append(near_pos)
        return None

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
        return count, requirements, frozenset(keys_found)


if __name__ == "__main__":
    main()

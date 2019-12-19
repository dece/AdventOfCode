import string
import sys

from grid import Grid


EX3 = [
    "#######",
    "#a.#Cd#",
    "##@#@##",
    "#######",
    "##@#@##",
    "#cB#Ab#",
    "#######",
]
EX4 = [
    "###############",
    "#d.ABC.#.....a#",
    "######@#@######",
    "###############",
    "######@#@######",
    "#b.....#.....c#",
    "###############",
]


def main():
    with open("day18.txt", "rt") as input_file:
        lines = input_file.readlines()
    print(f"Part 1 answer: {find_all_keys_with_min_steps(lines)} steps.")

    with open("day18-p2.txt", "rt") as input_file:  # yeah
        lines = input_file.readlines()
    print(f"Part 2 answer: {find_all_keys_with_min_steps(lines)} steps.")

def find_all_keys_with_min_steps(lines):
    """Find all keys with 1 or 4 starting points."""
    lab = Lab(lines=lines)
    lab.dumb_print()
    lab.find_positions()
    num_robots = len(lab.starts)
    states = [(
        lab.starts[0] if num_robots == 1 else encode_posis_packed(lab.starts),
        frozenset(),
        0
    )]
    state_cache = Grid(value_factory=dict)
    num_keys = len(lab.key_pos)
    min_steps = 2**32
    num_processed = 0
    while states:
        num_processed += 1
        one_or_more_pos, obtained, total_steps = states.pop(0)
        if len(obtained) == num_keys:
            print(f"[Found total of {total_steps}]", end="")
            min_steps = min(min_steps, total_steps)
            continue

        robot_positions = [one_or_more_pos] if num_robots == 1 else decode_posis(one_or_more_pos)
        for pos_index, pos in enumerate(robot_positions):
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
                    if num_robots > 1:
                        mpos = robot_positions.copy()
                        mpos[pos_index] = next_pos
                        next_pos = encode_posis_packed(tuple(mpos))
                    states.append((next_pos, next_obtained, next_steps))
                    old_bests[next_obtained] = next_steps
                print(".", end="")

        if num_processed % 100 == 0:
            print(f"[{num_processed}/{len(states)}]", end="")
        sys.stdout.flush()
    
    print()
    return min_steps

def encode_posis_packed(pt):
    p1, p2, p3, p4 = pt
    return encode_posis(p1, p2, p3, p4)

def encode_posis(p1, p2, p3, p4):
    return (
        (p1[0] << 24) + (p2[0] << 16) + (p3[0] << 8) + (p4[0]),
        (p1[1] << 24) + (p2[1] << 16) + (p3[1] << 8) + (p4[1]),
    )

def decode_posis(p):
    return [
        ((p[0] & 0xFF000000) >> 24, (p[1] & 0xFF000000) >> 24),
        ((p[0] & 0x00FF0000) >> 16, (p[1] & 0x00FF0000) >> 16),
        ((p[0] & 0x0000FF00) >>  8, (p[1] & 0x0000FF00) >> 8),
        ((p[0] & 0x000000FF)      , (p[1] & 0x000000FF)),
    ]


class Lab(Grid):

    TILE_PATH = "."
    TILE_WALL = "#"
    TILE_START = "@"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, value_factory=lambda: " ")
        self.starts = []
        self.key_pos = {}
        self.door_pos = {}

    def find_positions(self):
        for x, y, v in self.values_gen():
            if v == Lab.TILE_START:
                self.starts.append((x, y))
            if v in string.ascii_lowercase:
                self.key_pos[v] = (x, y)
            if v in string.ascii_uppercase:
                self.door_pos[v] = (x, y)
        for p in self.starts:
            self.setv(p[0], p[1], Lab.TILE_PATH)
    
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

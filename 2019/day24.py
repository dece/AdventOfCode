from collections import defaultdict

from grid import Grid


DIM = 5


def main():
    with open("day24.txt", "rt") as input_file:
        lines = input_file.readlines()

    # Part 1
    print("Part 1.")
    eris = Eris(value_factory=str, lines=lines)
    eris.dumb_print()
    snapshots = []
    while True:
        eris.step()
        ss = eris.snapshot()
        if ss in snapshots:
            break
        snapshots.append(ss)
    biorate = sum(2 ** i for i in range(DIM ** 2) if ss[i] == "#")
    print(f"Biodiv rate of first repeated layout: {biorate}.")

    # Part 2
    print("Part 2.")
    reris = RecursiveEris(lines)
    reris.levels[0].dumb_print()
    for i in range(200):
        reris.step()
    print(f"{reris.count_bugs()} bugs found.")


class Eris(Grid):

    def step(self):
        dying = []
        infesting = []
        for y in range(DIM ** 2):
            x = y % DIM
            y //= DIM
            v = self.getv(x, y)
            num_nears = sum(n == "#" for n in self.near_objects((x, y)).values())
            if v == "#" and num_nears != 1:
                dying.append((x, y))
            elif v == "." and num_nears in (1, 2):
                infesting.append((x, y))
        for p in dying:
            self.setv(p[0], p[1], ".")
        for p in infesting:
            self.setv(p[0], p[1], "#")

    def snapshot(self):
        return [self.getv(x, y) for y in range(DIM) for x in range(DIM)]


class RecursiveEris:

    def __init__(self, lines):
        self.levels = defaultdict(lambda: Grid(value_factory=lambda: "."))
        self.levels[0] = Grid(value_factory=lambda: ".", lines=lines)
        self.levels[1] = Grid(value_factory=lambda: ".")
        self.levels[-1] = Grid(value_factory=lambda: ".")

    def step(self):
        dying = []
        infesting = []
        for level_id in list(self.levels):
            level_dying, level_infesting = self.step_level(level_id)
            dying += level_dying
            infesting += level_infesting
        for p in dying:
            self.levels[p[0]].setv(p[1], p[2], ".")
        for p in infesting:
            self.levels[p[0]].setv(p[1], p[2], "#")

    def step_level(self, level_id):
        level_dying = []
        level_infesting = []
        for y in range(DIM ** 2):
            x = y % DIM
            y //= DIM
            if (x, y) == (2, 2):
                continue
            v = self.levels[level_id].getv(x, y)
            num_nears = sum(n == "#" for n in self.somewhat_near_objects(level_id, x, y).values())
            if v == "#" and num_nears != 1:
                level_dying.append((level_id, x, y))
            elif v == "." and num_nears in (1, 2):
                level_infesting.append((level_id, x, y))
        return level_dying, level_infesting

    def somewhat_near_objects(self, level_id, x, y):
        assert x in range(DIM) and y in range(DIM)
        current_level = self.levels[level_id]
        near_objs = {
            (level_id, x    , y - 1): current_level.getv(x    , y - 1),
            (level_id, x + 1, y    ): current_level.getv(x + 1, y    ),
            (level_id, x    , y + 1): current_level.getv(x    , y + 1),
            (level_id, x - 1, y    ): current_level.getv(x - 1, y    ),
        }
        for o in list(near_objs.keys()):
            ol, ox, oy = o
            # For outer level, just replace OOB pos with outer level tile value.
            lower_level = self.levels[ol - 1]
            if ox == -1:  # rightmost
                near_objs[(ol - 1, 1, 2)] = lower_level.getv(1, 2)
            elif ox == DIM:  # leftmost
                near_objs[(ol - 1, 3, 2)] = lower_level.getv(3, 2)
            if oy == -1:  # upmost
                near_objs[(ol - 1, 2, 1)] = lower_level.getv(2, 1)
            elif oy == DIM:  # downmost
                near_objs[(ol - 1, 2, 3)] = lower_level.getv(2, 3)
            # For inner level
            if o == (level_id, 2, 2):
                upper_level = self.levels[ol + 1]
                del near_objs[o]
                if x == 1:  # from the left
                    near_objs.update({(ol + 1, 0, iy): upper_level.getv(0, iy) for iy in range(DIM)})
                elif x == 3:  # from the right
                    near_objs.update({(ol + 1, DIM - 1, iy): upper_level.getv(DIM - 1, iy) for iy in range(DIM)})
                elif y == 1:  # from above
                    near_objs.update({(ol + 1, ix, 0): upper_level.getv(ix, 0) for ix in range(DIM)})
                else:  # y == 3, from below
                    near_objs.update({(ol + 1, ix, DIM - 1): upper_level.getv(ix, DIM - 1) for ix in range(DIM)})
        return near_objs
    
    def count_bugs(self):
        return sum(self.count_bugs_in(level_id) for level_id in self.levels)
    
    def count_bugs_in(self, level_id):
        return sum(v == "#" for _, _, v in self.levels[level_id].values_gen())


if __name__ == "__main__":
    main()

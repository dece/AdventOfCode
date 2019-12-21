from collections import defaultdict
from string import ascii_uppercase

from grid import Grid


def main():
    with open("day20.txt") as input_file:
        lines = [l.rstrip() for l in input_file.readlines()]

    # Part 1
    maze = Maze(lines)
    maze.find_portals()
    min_steps = maze.count_min_steps(maze.entry, maze.exit)
    print("Min steps:", min_steps)

    # Part 2
    maze = Maze(lines, recurse=True)
    maze.find_portals()
    min_steps = maze.count_min_steps(maze.entry, maze.exit)
    print("Min steps in recursion:", min_steps)


class Maze(Grid):

    TILE_PATH = "."
    TILE_WALL = "#"

    ENTRY_DG = "AA"
    EXIT_DG = "ZZ"

    def __init__(self, lines, recurse=False):
        super().__init__(value_factory=str, lines=lines)
        self.entry = None
        self.exit = None
        self.portals = {}
        self.recurse = recurse
        self.portal_is_outer = {}
        self.height = len(lines)
        self.width = max(len(line) for line in lines)

    def find_portals(self):
        portals = defaultdict(list)
        for x, y, v in list(self.values_gen()):
            if v in ascii_uppercase:
                rv = self.getv(x + 1, y)
                if rv and rv in ascii_uppercase:
                    rrv = self.getv(x + 2, y)
                    portal_pos = (x + 2, y) if rrv == Maze.TILE_PATH else (x - 1, y)
                    portals[v + rv].append(portal_pos)
                    self.portal_is_outer[portal_pos] = x == 0 or x == self.width - 2
                    continue
                dv = self.getv(x, y + 1)
                if dv and dv in ascii_uppercase:
                    ddv = self.getv(x, y + 2)
                    portal_pos = (x, y + 2) if ddv == Maze.TILE_PATH else (x, y - 1)
                    portals[v + dv].append(portal_pos)
                    self.portal_is_outer[portal_pos] = y == 0 or y == self.height - 2
        self.entry = portals["AA"][0]
        self.exit = portals["ZZ"][0]
        for p in portals.values():
            if len(p) == 2:
                self.portals[p[0]] = p[1]
                self.portals[p[1]] = p[0]

    def dumb_print(self, rpos=None, level=0):
        for y, row in self.g.items():
            for x, v in row.items():
                pos = (x, y)
                if pos == rpos:
                    v = "@"
                elif pos in (self.entry, self.exit):
                    v = "▒" if not self.recurse or level == 0 else "#"
                elif pos in self.portals:
                    v = "▒" if not self.recurse or level > 0 or not self.portal_is_outer[pos] else "#"
                print(v, end="")
            print()

    def bfs(self, start, end):
        discovered = defaultdict(lambda: Grid(value_factory=bool))
        discovered[0].setv(start[0], end[1], True)
        parents = {}
        q = [(start, 0)]
        while q:
            pos, level = q.pop(0)
            if pos == end and (not self.recurse or level == 0):
                return parents
            nears = self.near_objects(pos)
            is_portal = pos in self.portals
            if is_portal:
                nears[self.portals[pos]] = Maze.TILE_PATH
            for near_pos, near_tile in nears.items():
                if near_tile != Maze.TILE_PATH:
                    continue
                near_level = level
                if self.recurse and is_portal and near_pos == self.portals[pos]:
                    near_level += -1 if self.portal_is_outer[pos] else 1
                if near_level < 0 or discovered[near_level].getv(near_pos[0], near_pos[1]):
                    continue
                discovered[near_level].setv(near_pos[0], near_pos[1], True)
                parents[(near_pos, near_level)] = (pos, level)
                q.append((near_pos, near_level))
        return None

    def count_min_steps(self, start, end):
        parents = self.bfs(start, end)
        count = 0
        pos = (end, 0)
        while pos != (start, 0):
            count += 1
            parent = parents[pos]
            pos = parent
        return count


if __name__ == "__main__":
    main()

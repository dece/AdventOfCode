from collections import defaultdict
from string import ascii_uppercase

from grid import Grid


def main():
    with open("day20.txt") as input_file:
        lines = [l.rstrip() for l in input_file.readlines()]
    maze = Maze(lines, value_factory=str)

    maze.find_portals()
    maze.dumb_print()
    min_steps = maze.count_min_steps(maze.entry, maze.exit)
    print("Min steps:", min_steps)


class Maze(Grid):
    
    TILE_PATH = "."
    TILE_WALL = "#"

    ENTRY_DG = "AA"
    EXIT_DG = "ZZ"

    def __init__(self, lines, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entry = None
        self.exit = None
        self.portals = {}
        for y, line in enumerate(lines):
            for x, value in enumerate(line):
                self.setv(x, y, value)

    def find_portals(self):
        portals = defaultdict(list)
        for x, y, v in list(self.values_gen()):
            if v in ascii_uppercase:
                rv = self.getv(x + 1, y)
                if rv and rv in ascii_uppercase:
                    rrv = self.getv(x + 2, y)
                    portal_pos = (x + 2, y) if rrv == Maze.TILE_PATH else (x - 1, y)
                    portals[v + rv].append(portal_pos)
                    continue
                dv = self.getv(x, y + 1)
                if dv and dv in ascii_uppercase:
                    ddv = self.getv(x, y + 2)
                    portal_pos = (x, y + 2) if ddv == Maze.TILE_PATH else (x, y - 1)
                    portals[v + dv].append(portal_pos)
        for n, p in portals.items():
            if n == "AA":
                self.entry = p[0]
            elif n == "ZZ":
                self.exit = p[0]
            else:
                self.portals[p[0]] = p[1]
                self.portals[p[1]] = p[0]
    
    def dumb_print(self):
        for y, row in self.g.items():
            for x, v in row.items():
                if (x, y) in self.portals:
                    v = "░"
                if (x, y) in (self.entry, self.exit):
                    v = "▒"
                print(v, end="")
            print()

    def bfs(self, start, end):
        discovered = Grid(value_factory=bool)
        discovered.setv(start[0], end[1], True)
        parents = {}
        q = [start]
        while q:
            pos = q.pop(0)
            if pos == end:
                return parents
            nears = self.near_objects(pos)
            for near_pos, near_tile in nears.items():
                if near_tile != Maze.TILE_PATH:
                    continue
                if discovered.getv(near_pos[0], near_pos[1]):
                    continue
                discovered.setv(near_pos[0], near_pos[1], True)
                parents[near_pos] = pos
                q.append(near_pos)
        return None
    
    def count_min_steps(self, start, end):
        parents = self.bfs(start, end)
        count = 0
        pos = end
        while pos != start:
            pos = parents[pos]
            count += 1
            if pos in self.portals:  # One more step to traverse portal.
                count += 1
        return count
    
    def near_objects(self, p):
        nears = super().near_objects(p)
        for near in list(nears):
            if near in self.portals:
                nears[self.portals[near]] = Maze.TILE_PATH
        return nears


if __name__ == "__main__":
    main()

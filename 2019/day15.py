from collections import defaultdict
import time 

from intcode import Intcode


def main():
    with open("day15.txt", "rt") as input_file:
        text = input_file.readlines()[0].rstrip()
    codes = Intcode.parse_input(text)

    # Part 1
    droid = Droid(codes)
    droid.run()
    print(f"Oxygen system at {droid.oxygen_system_pos}.")
    parents = bfs(droid.tiles, (0, 0), droid.oxygen_system_pos)
    num_steps = len_backtrack(parents, droid.oxygen_system_pos, (0, 0))
    print(f"{num_steps} steps with BFS.")

    # Part 2
    os_pos = droid.oxygen_system_pos
    droid.tiles[os_pos[0]][os_pos[1]] = Droid.TILE_O2
    minutes = 0
    propagations = [os_pos]
    while propagations:
        next_propagations = []
        for prop in propagations:
            adjacents = list(filter(
                lambda p: droid.tiles[p[0]][p[1]] == Droid.TILE_CLR,
                [Droid.forward(prop, d[1]) for d in Droid.NEXT_DIR.keys()]
            ))
            for adj in adjacents:
                droid.tiles[adj[0]][adj[1]] = Droid.TILE_O2
            next_propagations += adjacents
        if not next_propagations:
            break
        propagations = next_propagations

        droid.draw()
        minutes += 1
        print(f"Minute {minutes}: propagated to {propagations}")
        time.sleep(0.2)
        

class Droid(Intcode):

    TILE_UNK = 0
    TILE_WALL = 1
    TILE_CLR = 2
    TILE_O2 = 4

    RES_COLL = 0
    RES_OK = 1
    RES_END = 2

    DIR_N = 1, (+1, 0)
    DIR_S = 2, (-1, 0)
    DIR_W = 3, (0, -1)
    DIR_E = 4, (0, +1)

    NEXT_DIR = {
        DIR_N: DIR_E,
        DIR_S: DIR_W,
        DIR_W: DIR_N,
        DIR_E: DIR_S,
    }
    PREV_DIR = {v: k for k, v in NEXT_DIR.items()}

    def __init__(self, codes):
        super().__init__(codes)
        self.tiles = defaultdict(lambda: defaultdict(lambda: Droid.TILE_UNK))
        self.x = 0
        self.y = 0
        self.steps = 0
        self.oxygen_system_pos = None
        self.dir = Droid.DIR_N

    def input_data(self):
        self.steps += 1
        return self.dir[0]

    def output_data(self, data):
        fx, fy = self.get_forward_pos()
        if data == Droid.RES_COLL:
            self.tiles[fx][fy] = Droid.TILE_WALL
            self.dir = Droid.NEXT_DIR[self.dir]
        else:
            self.x, self.y = fx, fy
            self.dir = Droid.PREV_DIR[self.dir]
            self.tiles[self.x][self.y] = Droid.TILE_CLR
            if data == Droid.RES_END:
                self.oxygen_system_pos = self.x, self.y
            self.halt = (fx, fy) == (0, 0)
        if self.halt:
            self.draw()
    
    def get_forward_pos(self):
        return Droid.forward((self.x, self.y), self.dir[1])
    
    @staticmethod
    def forward(pos, dirv):
        return pos[0] + dirv[0], pos[1] + dirv[1]

    def draw(self):
        for x in range(-24, 24):
            for y in range(-24, 24):
                if (x, y) == self.oxygen_system_pos:
                    print("@", end="")
                elif (x, y) == (0, 0):
                    print("s", end="")
                elif (x, y) == (self.x, self.y):
                    print("D", end="")
                else:
                    print({
                        Droid.TILE_UNK: " ",
                        Droid.TILE_WALL: "█",
                        Droid.TILE_CLR: "░",
                        Droid.TILE_O2: "▒",
                    }[self.tiles[x][y]], end="")
            print()


def bfs(tiles, start, end):
    discovered = defaultdict(lambda: defaultdict(bool))
    discovered[start[0]][start[1]] = True
    parents = {}
    q = [start]
    while q:
        pos = q.pop(0)
        if pos == end:
            return parents
        adjacents = filter(
            lambda p: tiles[p[0]][p[1]] != Droid.TILE_WALL,
            [Droid.forward(pos, d[1]) for d in Droid.NEXT_DIR.keys()]
        )
        for adj in adjacents:
            if discovered[adj[0]][adj[1]]:
                continue
            discovered[adj[0]][adj[1]] = True
            parents[adj] = pos
            q.append(adj)

def len_backtrack(parents, x, end):
    count = 0
    while x != end:
        x = parents[x]
        count += 1
    return count


if __name__ == "__main__":
    main()

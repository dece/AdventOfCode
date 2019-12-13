import time

from intcode import Intcode


def main():
    with open("day13.txt", "rt") as input_file:
        text = input_file.readlines()[0].rstrip()
    codes = Intcode.parse_input(text)
    
    # Part 1
    game = Game(codes)
    game.run()
    print("Num block tiles:", sum(sum(v == Game.TILE_BLOCK for v in row) for row in game.tiles))

    # Part 2 (autoplay)
    codes[0] = 2
    game = DemoGame(codes)
    game.run()


class Game(Intcode):

    TILES_DIM = 64

    TILE_EMPTY = 0
    TILE_WALL = 1
    TILE_BLOCK = 2
    TILE_HPAD = 3
    TILE_BALL = 4

    TILES_CHARS = {
        TILE_EMPTY: " ",
        TILE_WALL: "█",
        TILE_BLOCK: "░",
        TILE_HPAD: "▔",
        TILE_BALL: "o",
    }

    OUT_X = 0
    OUT_Y = 1
    OUT_T = 2

    JOY_L = -1
    JOY_N = 0
    JOY_R = 1

    def __init__(self, codes, debug=False):
        super().__init__(codes, debug=debug)
        self.tiles = [[Game.TILE_EMPTY] * Game.TILES_DIM for _ in range(Game.TILES_DIM)]
        self.output_type = Game.OUT_X
        self.output_pos = [0, 0]

    def input_data(self):
        self.print_tiles()
        return int({
            "h": Game.JOY_L,
            "l": Game.JOY_R,
        }.get(input(), Game.JOY_N))

    def output_data(self, data):
        if self.output_type in [self.OUT_X, self.OUT_Y]:
            self.output_pos[self.output_type] = data
        elif self.output_type == self.OUT_T:
            if self.output_pos == [-1, 0]:
                print("Score:", data)
            else:
                self.tiles[self.output_pos[1]][self.output_pos[0]] = data
        self.output_type = (self.output_type + 1) % 3
    
    def print_tiles(self):
        for row in self.tiles:
            if row[0] == Game.TILE_EMPTY:
                break
            for value in row:
                print(Game.TILES_CHARS[value], end="")
            print()


class DemoGame(Game):

    def input_data(self):
        ball_pos = self.get_unique_tile_pos(Game.TILE_BALL)
        pad_pos = self.get_unique_tile_pos(Game.TILE_HPAD)
        self.print_tiles()
        time.sleep(0.1)
        if ball_pos[1] > pad_pos[1]:
            return Game.JOY_R
        elif ball_pos[1] < pad_pos[1]:
            return Game.JOY_L
        else:
            return Game.JOY_N

    def get_unique_tile_pos(self, tile_id):
        for x, row in enumerate(self.tiles):
            for y, value in enumerate(row):
                if value == tile_id:
                    return [x, y]
        raise ValueError("Could not find {}".format(tile_id))


if __name__ == "__main__":
    main()

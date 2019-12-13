from intcode import Intcode


def main():
    with open("day13.txt", "rt") as input_file:
        text = input_file.readlines()[0].rstrip()
    codes = Intcode.parse_input(text)
    
    game = Game(codes, debug=False)
    game.run()
    print("Num block tiles:", sum(sum(v == Game.TILE_BLOCK for v in row) for row in game.tiles))


class Game(Intcode):

    TILES_DIM = 64

    TILE_EMPTY = 0
    TILE_WALL = 1
    TILE_BLOCK = 2
    TILE_HPAD = 3
    TILE_BALL = 4

    OUT_X = 0
    OUT_Y = 1
    OUT_T = 2

    def __init__(self, codes, debug=False):
        super().__init__(codes, debug=debug)
        self.tiles = [[Game.TILE_EMPTY] * Game.TILES_DIM for _ in range(Game.TILES_DIM)]
        self.output_type = Game.OUT_X
        self.output_pos = [0, 0]

    def output_data(self, data):
        if self.output_type in [self.OUT_X, self.OUT_Y]:
            self.output_pos[self.output_type] = data
        elif self.output_type == self.OUT_T:
            self.tiles[self.output_pos[1]][self.output_pos[0]] = data
        self.output_type = (self.output_type + 1) % 3
    
    def print_tiles(self):
        for row in self.tiles:
            for value in row:
                print(str(value), end="")
            print()


if __name__ == "__main__":
    main()

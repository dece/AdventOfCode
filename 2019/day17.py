from collections import defaultdict

from grid import Grid
from intcode import Intcode


def main():
    with open("day17.txt", "rt") as input_file:
        codes = Intcode.parse_input(input_file.read().rstrip())
    
    camera = Camera(codes)
    camera.run()
    intersections = camera.intersect()
    print("Sum:", sum(x * y for x, y in intersections))


class Camera(Intcode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.out_x = 0
        self.out_y = 0
        self.img = Grid()

    def output_data(self, data):
        if data == ord("\n"):
            self.out_x, self.out_y = 0, self.out_y + 1
        else:
            self.img.g[self.out_y][self.out_x] = data
            self.out_x += 1

    def intersect(self):
        intersections = []
        g = self.img.g
        for x, col in list(g.items()).copy():
            for y, v in list(col.items()).copy():
                if all(
                    e == ord("#")
                    for e in [v, g[x][y-1], g[x][y+1], g[x+1][y], g[x-1][y]]
                ):
                    print("O", end="")
                    intersections.append((x, y))
                else: 
                    print(chr(v), end="")
            print()
        return intersections


if __name__ == "__main__":
    main()

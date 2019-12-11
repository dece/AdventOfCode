from queue import Queue

from PIL import Image

from intcode import Intcode


def main():
    with open("day11.txt", "rt") as input_file:
        text = input_file.readlines()[0].rstrip()
    codes = Intcode.parse_input(text)

    # Part 1
    robot = Robot(codes)
    robot.run()
    print("Num painted:", robot.get_num_painted())

    # Part 2
    robot = Robot(codes, draw=True)
    robot.set_paint(1)
    robot.run()
    robot.save_image("/tmp/day11.png")


class Robot(Intcode):

    OP_PAINT = 0
    OP_TURN = 1

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self, codes, debug=False, draw=False):
        super().__init__(codes, debug=debug)
        self.panel = {}
        self.x = 0
        self.y = 0
        self.direction = self.UP
        self.output_type = self.OP_PAINT
        self.image = Image.new("1", (100, 100)) if draw else None

    def input_data(self):
        return self.get_paint()

    def output_data(self, data):
        if self.output_type == self.OP_PAINT:
            self.set_paint(data)
            self.output_type = self.OP_TURN
        elif self.output_type == self.OP_TURN:
            self.direction += 1 if data == 1 else -1
            self.move()
            self.output_type = self.OP_PAINT

    def move(self):
        self.x, self.y = {
            self.UP: (self.x + 1, self.y),
            self.RIGHT: (self.x, self.y + 1),
            self.DOWN: (self.x - 1, self.y),
            self.LEFT: (self.x, self.y - 1),
        }[self.get_direction()]

    def get_direction(self):
        return self.direction % 4

    def get_paint(self):
        if self.x not in self.panel or self.y not in self.panel[self.x]:
            self.set_paint(0)
        return self.panel[self.x][self.y]

    def set_paint(self, color):
        if self.x not in self.panel:
            self.panel[self.x] = {}
        self.panel[self.x][self.y] = color
        if self.image:
            self.image.putpixel((self.x - 1, self.y - 1), color)

    def get_num_painted(self):
        return sum(len(row.values()) for row in self.panel.values())

    def save_image(self, path):
        if self.image:
            self.image.rotate(90).save(path)


if __name__ == "__main__":
    main()

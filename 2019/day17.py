from grid import Grid
from intcode import Intcode
from vector import *


def main():
    with open("day17.txt", "rt") as input_file:
        codes = Intcode.parse_input(input_file.read().rstrip())
    
    # Part 1
    robot = Robot(codes)
    robot.run()
    intersections = robot.intersect()
    print("Sum:", sum(x * y for x, y in intersections))

    # Part 2
    start = robot.start
    sx, sy, so = start
    print(f"Start at {(sx, sy)} oriented {so}.")
    path = compute_path(robot.img, start)
    print(f"Traced path: {path}.")
    # Patterns found in my editor from the above result...
    patterns = {
        "M": "ABBACBCCBA",
        "A": ['R', 10, 'R', 8, 'L', 10, 'L', 10],
        "B": ['R', 8, 'L', 6, 'L', 6],
        "C": ['L', 10, 'R', 10, 'L', 6],
    }
    codes[0] = 2
    robot = Robot(codes, patterns=patterns, video_fb=False)
    robot.run()


N = ord("\n")
S = ord("#")


class Robot(Intcode):

    ORI_U = (0, -1)
    ORI_R = (1, 0)
    ORI_D = (0, +1)
    ORI_L = (-1, 0)
    ORI_INDEXES = {ORI_U: 0, ORI_R: 1, ORI_D: 2, ORI_L: 3}
    ASCII_ORI = {"^": ORI_U, ">": ORI_R, "v": ORI_D, "<": ORI_L}

    def __init__(self, *args, patterns=None, video_fb=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.out_x = 0
        self.out_y = 0
        self.img = Grid()
        self.start = None
        self.moving = False
        self.video_fb = video_fb
        self.video_last_byte = None
        self.patterns = patterns
        self.robot_inputs = []
        if self.patterns:
            self.input_gen()

    def input_data(self):
        self.moving = True
        data = self.robot_inputs.pop(0)
        return data
    
    def input_gen(self):
        self.robot_inputs += [ord(x) for x in ",".join(self.patterns["M"])] + [N]
        for pname in "ABC":
            pdata = ",".join(map(lambda x: str(x), self.patterns[pname]))
            self.robot_inputs += [ord(x) for x in pdata] + [N]
        self.robot_inputs += [ord("y" if self.video_fb else "n"), N]

    def output_data(self, data):
        if data > 256:
            print("Output", data)
            return
        
        if self.video_fb:
            print(chr(data), end="")
            if all(d == N for d in [data, self.video_last_byte]):
                input()
            self.video_last_byte = data
        if self.moving:
            return

        if data == N:
            self.out_x, self.out_y = 0, self.out_y + 1
        else:
            self.img.g[self.out_y][self.out_x] = data
            self.out_x += 1

    def intersect(self):
        intersections = []
        g = self.img.g
        for y, row in list(g.items()).copy():
            for x, v in list(row.items()).copy():
                if all(e == S for e in [v, g[y][x-1], g[y][x+1], g[y+1][x], g[y-1][x]]):
                    intersections.append((x, y))
                elif chr(v) in Robot.ASCII_ORI.keys():
                        self.start = (x, y, Robot.ASCII_ORI[chr(v)])
        return intersections


def compute_path(grid, start):
    pos, o = (start[0], start[1]), start[2]
    path = []
    steps = 0
    while True:        
        forward_pos = v2a(pos, o)
        near_pos = grid.near_items(pos)
        if near_pos[forward_pos] == S:
            pos = forward_pos
            steps += 1
            continue
        if steps:
            path.append(steps)
        steps = 0
        
        for n in [p for p, v in near_pos.items() if v == S]:
            res = turn(pos, n, o)
            if res is not None:
                path.append(res[0])
                o = res[1]
                break
        else:
            break

    return path

def turn(pos, next_pos, cur_ori):
    new_ori = (next_pos[0] - pos[0], next_pos[1] - pos[1])
    diff = (Robot.ORI_INDEXES[new_ori] - Robot.ORI_INDEXES[cur_ori]) % 4
    if diff == 1:
        return "R", new_ori
    elif diff == 3:
        return "L", new_ori


if __name__ == "__main__":
    main()

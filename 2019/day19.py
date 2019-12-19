from grid import Grid
from intcode import Intcode


def main():
    codes = Intcode.parse_file("day19.txt")
    mgr = DroneMgr(codes)

    # Part 1
    area = Grid()
    for y in range(50):
        for x in range(50):
            mgr.run(inputs=[x, y])
            area.setv(y, x, mgr.clear())
    area.dumb_print()
    num_affected = sum(v for _, _, v in area.values_gen())
    print("Num affected:", num_affected)

    # Part 2
    d = 100 - 1
    found = None
    x, y = 0, 4  # skip beam being too narrow for grid
    while not found:
        y += 1
        while True:
            mgr.run(inputs=[x, y])
            if mgr.clear() == 0:
                x += 1
                continue
            mgr.run(inputs=[x + d, y - d])
            if mgr.clear() == 1:
                found = (x, y - d)
            break
    print("Found 100x100 ship with nearest corner at", found)
    print("Answer:", found[0] * 10000 + found[1])


class DroneMgr(Intcode):
    
    def __init__(self, program, *args, **kwargs):
        super().__init__(program, *args, **kwargs)
        self.program = program.copy()
        self.output = None

    def clear(self):
        output = self.output
        self.reset()
        self.output = None
        return output

    def output_data(self, data):
        self.output = data


if __name__ == "__main__":
    main()

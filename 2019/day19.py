from grid import Grid
from intcode import Intcode
from tools import parse_intcode


def main():
    codes = parse_intcode("day19.txt")
    area = Grid()
    for y in range(50):
        for x in range(50):
            mgr = DroneMgr(codes)
            mgr.run(inputs=[x, y])
            area.setv(x, y, mgr.output)
    area.dumb_print()
    num_affected = sum(v for _, _, v in area.values_gen())
    print("Num affected:", num_affected)


class DroneMgr(Intcode):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inputs = [0, 0]
        self.output = None

    def output_data(self, data):
        self.output = data


if __name__ == "__main__":
    main()

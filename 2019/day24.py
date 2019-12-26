from grid import Grid


DIM = 5


def main():
    with open("day24.txt", "rt") as input_file:
        lines = input_file.readlines()
    eris = Eris(value_factory=str, lines=lines)
    eris.dumb_print()
    print()

    snapshots = []
    while True:
        eris.dumb_print()
        eris.step()
        ss = eris.snapshot()
        if ss in snapshots:
            break
        snapshots.append(ss)
    biorate = sum(2 ** i for i in range(DIM ** 2) if ss[i] == "#")
    print(f"Biodiv rate of first repeated layout: {biorate}.")


class Eris(Grid):

    def step(self):
        dying = []
        infesting = []
        for y in range(DIM ** 2):
            x = y % DIM
            y //= DIM
            v = self.getv(x, y)
            num_nears = sum(n == "#" for n in self.near_objects((x, y)).values())
            if v == "#" and num_nears != 1:
                dying.append((x, y))
            elif v == "." and num_nears in (1, 2):
                infesting.append((x, y))
        for p in dying:
            self.setv(p[0], p[1], ".")
        for p in infesting:
            self.setv(p[0], p[1], "#")

    def snapshot(self):
        return [self.getv(x, y) for y in range(DIM) for x in range(DIM)]


if __name__ == "__main__":
    main()

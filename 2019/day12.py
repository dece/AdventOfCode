from copy import deepcopy
import itertools
import re

import numpy


def main():
    with open("day12.txt", "rt") as input_file:
        lines = input_file.readlines()
    vector_re = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")
    matches = [vector_re.match(line.rstrip()) for line in lines]
    coords = [[int(i) for i in match.groups()] for match in matches]
    moons_i = [[coord, [0] * 3] for coord in coords]

    # Part 1
    moons = deepcopy(moons_i)
    for _ in range(1000):
        do_step(moons)
    print("Total moons energy:", sum(get_energy(moon) for moon in moons))

    # Part 2
    d_cycles = [0] * 3
    for d in range(3):
        moons = deepcopy(moons_i)
        step = 0
        found_d_cycle = False
        while not found_d_cycle:
            do_step(moons)
            step += 1
            for moon, moon_i in zip(moons, moons_i):
                if moon[0][d] != moon_i[0][d] or moon[1][d] != moon_i[1][d]:
                    break
            else:
                d_cycles[d] = step
                found_d_cycle = True
    print("Dimension cycles:", d_cycles)
    print("LCM:", numpy.lcm.reduce(d_cycles))

def do_step(moons):
    for a, b in itertools.combinations(moons, 2):
        for d in range(3):
            if a[0][d] > b[0][d]:
                a[1][d] -= 1
                b[1][d] += 1
            elif a[0][d] < b[0][d]:
                a[1][d] += 1
                b[1][d] -= 1

    for moon in moons:
        for d in range(3):
            moon[0][d] += moon[1][d]

def get_energy(moon):
    pot = sum(abs(moon[0][d]) for d in range(3))
    ket = sum(abs(moon[1][d]) for d in range(3))
    return pot * ket


if __name__ == "__main__":
    main()

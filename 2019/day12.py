import itertools
import re



def main():
    with open("day12.txt", "rt") as input_file:
        lines = input_file.readlines()
    vector_re = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")
    matches = [vector_re.match(line.rstrip()) for line in lines]
    coords = [list([int(i) for i in match.groups()]) for match in matches]
    moons = [[coord, [0] * 3] for coord in coords]

    # Part 1
    for _ in range(1000):
        do_step(moons)
    print("Total moons energy:", sum(get_energy(moon) for moon in moons))

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

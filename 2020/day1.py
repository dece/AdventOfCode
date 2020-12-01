import itertools


def main():
    with open("day1.txt", "rt") as f:
        lines = [line.rstrip() for line in f.readlines()]
    values = list(map(lambda l: int(l), lines))

    # Part 1
    for a, b in itertools.combinations(values, 2):
        if a + b == 2020:
            print(a * b)
    # Part 2
    for a, b, c in itertools.combinations(values, 3):
        if a + b + c == 2020:
            print(a * b * c)


if __name__ == "__main__":
    main()

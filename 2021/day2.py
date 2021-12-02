import sys


def main():
    lines = [line.rstrip() for line in sys.stdin]

    # Part 1
    hor = 0
    depth = 0
    for line in lines:
        d, n = line.split()
        if d[0] == "f":
            hor += int(n)
        elif d[0] == "d":
            depth += int(n)
        elif d[0] == "u":
            depth -= int(n)
    print(hor * depth)

    # Part 2
    aim = 0
    hor = 0
    depth = 0
    for line in lines:
        d, n = line.split()
        if d[0] == "f":
            hor += int(n)
            depth += int(n) * aim
        elif d[0] == "d":
            aim += int(n)
        elif d[0] == "u":
            aim -= int(n)
    print(hor * depth)


if __name__ == "__main__":
    main()

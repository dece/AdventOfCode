import sys


def main():
    lines = [line.rstrip() for line in sys.stdin]
    data = {k: 0 for k in range(1, 6)}
    for n in map(int, lines[0].split(",")):
        data[n] += 1

    # Part 1
    for _ in range(80):
        data = step(data)
    print(sum(data.values()))

    # Part 2
    for _ in range(256 - 80):
        data = step(data)
    print(sum(data.values()))


def step(data):
    next_data = {k: 0 for k in range(1, 9)}
    for k, v in data.items():
        if v == 0:
            continue
        if k == 0:
            next_data[6] += v
            next_data[8] += v
        else:
            next_data[k - 1] = v
    return next_data


if __name__ == "__main__":
    main()

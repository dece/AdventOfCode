import sys


def main():
    lines = [line.rstrip() for line in sys.stdin]
    positions = list(map(int, lines[0].split(",")))
    solve(positions, lambda x, y: abs(x - y))
    solve(positions, lambda x, y: sum(range(abs(x - y) + 1)))


def solve(positions, acc_f):
    a, b = min(positions), max(positions)
    while True:
        mid = (a + b) // 2
        conso = consume(positions, mid, acc_f)
        conso_up = consume(positions, mid + 1, acc_f)
        conso_down = consume(positions, mid - 1, acc_f)
        if conso < conso_up and conso < conso_down:
            break
        if conso_up < conso:
            a = mid
        else:
            b = mid
    print(conso)


def consume(positions, toward, acc_f):
    return sum(acc_f(pos, toward) for pos in positions)


if __name__ == "__main__":
    main()

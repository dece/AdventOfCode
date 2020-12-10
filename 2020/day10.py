import sys


def main():
    lines = sorted([int(line.rstrip()) for line in sys.stdin])
    
    # Part 1
    diffs = {1: 0, 3: 0}
    jojo = 0
    for v in lines:
        d = v - jojo
        diffs[d] += 1
        jojo = v
    print("Part 1:", diffs[1] * (diffs[3] + 1))

    # Part 2 - yes recursion is fine but have you tried caching your damn values
    print("Part 2:", rec(0, lines, 0, len(lines), {}))


def rec(i, l, n, z, c):
    if i >= z - 1:
        return 1
    if (p := c.get((i, n))) is not None:
        return p
    p = 0
    for ni, nv in enumerate(l[i:i+3]):
        if n < nv <= n + 3:
            p += rec(i + ni + 1, l, nv, z, c)
    c[(i, n)] = p
    return p


if __name__ == "__main__":
    main()

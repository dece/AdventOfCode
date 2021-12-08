import sys


def main():
    lines = [line.rstrip() for line in sys.stdin]
    data = [tuple(map(str.split, line.split(" | "))) for line in lines]

    # Part 1
    print(sum(
        n in (2, 4, 3, 7)  # num enabled for 1, 4, 7, 8 resp.
        for values in map(lambda l: l[1], data)
        for n in map(len, values)
    ))

    # Part 2
    print(sum(map(solve, data)))


def solve(line):
    patterns, values = line
    P = [None] * 10
    P[1] = next(p for p in patterns if len(p) == 2)  # cf
    P[4] = next(p for p in patterns if len(p) == 4)  # bcdf
    P[7] = next(p for p in patterns if len(p) == 3)  # acf
    P[8] = next(p for p in patterns if len(p) == 7)  # abcdefg
    conn_a = next(c for c in P[7] if c not in P[1])
    P[9] = next(
        p for p in patterns
        if len(p) == 6 and all(c in p for c in P[4] + conn_a)
    )
    P[3] = next(
        p for p in patterns
        if len(p) == 5 and all(c in p for c in P[1])
    )
    conn_g = next(c for c in P[9] if c not in P[4] + conn_a)
    conn_d = next(c for c in P[3] if c not in P[7] and c != conn_g)
    P[0] = next(p for p in patterns if len(p) == 6 and conn_d not in p)
    remaining = [p for p in patterns if p not in P]
    P[6] = next(p for p in remaining if len(p) == 6)
    remaining.remove(P[6])
    P[5] = next(p for p in remaining if all(c in P[6] for c in p))
    remaining.remove(P[5])
    P[2] = remaining[0]
    mamap = {"".join(sorted(P[i])): i for i in range(10)}
    return sum(
        mamap["".join(sorted(value))] * (10**i)
        for i, value in enumerate(reversed(values))
    )


if __name__ == "__main__":
    main()

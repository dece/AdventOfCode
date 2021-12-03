import sys


def main():
    lines = [line.rstrip() for line in sys.stdin]

    # Part 1
    cumul = [0] * len(lines[0])
    for line in lines:
        for i, b in enumerate(line):
            cumul[i] += 1 if b == "1" else -1
    gamma = int("".join(map(lambda n: "1" if n > 0 else "0", cumul)), 2)
    epsilon = gamma ^ (2 ** len(cumul) - 1)  # why does ~ not work? ugly mask
    print(gamma * epsilon)

    # Part 2
    ogr_values = lines[:]
    csr_values = lines[:]
    for i in range(len(cumul)):
        if len(ogr_values) > 1:
            cumul = sum(1 if v[i] == "1" else -1 for v in ogr_values)
            ogr_mc = 1 if cumul >= 0 else 0
            ogr_values = [v for v in ogr_values if int(v[i]) == ogr_mc]
        if len(csr_values) > 1:
            cumul = sum(1 if v[i] == "1" else -1 for v in csr_values)
            csr_lc = 0 if cumul >= 0 else 1
            csr_values = [v for v in csr_values if int(v[i]) == csr_lc]
    print(int(ogr_values[0], 2) * int(csr_values[0], 2))


if __name__ == "__main__":
    main()

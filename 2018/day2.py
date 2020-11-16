def main():
    with open("day2.txt", "rt") as f:
        lines = [line.rstrip() for line in f.readlines()]

    n2 = 0
    n3 = 0
    for line in lines:
        occurences = [line.count(letter) for letter in line]
        if 2 in occurences:
            n2 += 1
        if 3 in occurences:
            n3 += 1
    print(n2 * n3)

    for line in lines:
        for other in lines:
            diffs = 0
            common = ""
            for c1, c2 in zip(line, other):
                if c1 == c2:
                    common += c1
                else:
                    diffs += 1
            if diffs == 1:
                print(common)
                return


if __name__ == "__main__":
    main()

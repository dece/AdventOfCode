def main():
    with open("day2.txt", "rt") as f:
        lines = [line.rstrip() for line in f.readlines()]
    # Part 1
    valid = 0
    for line in lines:
        count, letter, password = line.split()
        min_n, max_n = count.split("-")
        letter = letter.rstrip(":")
        if int(min_n) <= password.count(letter) <= int(max_n):
            valid += 1
    print("Valids:", valid)
    # Part 2
    valid = 0
    for line in lines:
        count, letter, password = line.split()
        ofs_a, ofs_b = count.split("-")
        letter = letter.rstrip(":")
        a = password[int(ofs_a) - 1]
        b = password[int(ofs_b) - 1]
        if (a == letter or b == letter) and not (a == b == letter):
            valid += 1
    print("Valids:", valid)


if __name__ == "__main__":
    main()

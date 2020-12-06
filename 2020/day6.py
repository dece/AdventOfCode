def main():
    with open("day6.txt", "rt") as f:
        text = f.read()
    groups = text.split("\n\n")

    # Part 1
    count = 0
    for g in groups:
        letters = set(g)
        count += len(letters)
        if "\n" in g:
            count -= 1
    print("Total:", count)

    # Part 2
    count = 0
    for g in groups:
        common = None
        answers = [set(p) for p in g.split("\n") if p]
        for a in answers:
            common = set(a) if common is None else common & set(a)
        count += len(common)
    print("Commons:", count)


if __name__ == "__main__":
    main()

EX = "FBFBBFFRLR"


def main():
    with open("day5.txt", "rt") as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    # Part 1
    ids = [get_id(c) for c in lines]
    print("Max seat ID:", max(ids))

    # Part 2
    for i in range(min(ids), max(ids)):
        if i not in ids and i-1 in ids and i+1 in ids:
            print("Happy little seat:", i)
            break


def get_id(code):
    row_base, row_part = 0, 128
    col_base, col_part = 0, 8
    for c in code:
        if c == "F":
            row_part //= 2
        elif c == "B":
            row_part //= 2
            row_base += row_part
        elif c == "L":
            col_part //= 2
        elif c == "R":
            col_part //= 2
            col_base += col_part
    return row_base * 8 + col_base
    # so you're saying it was actually binary?... it's 3AM here.


if __name__ == "__main__":
    main()

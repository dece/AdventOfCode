import sys

def main():
    lines = [line.rstrip() for line in sys.stdin]

    # Part 1
    cups = list(map(int, lines[0]))
    for _ in range(100):
        move(cups)
    while cups[0] != 1:
        cups.append(cups.pop(0))
    print("Part 1:", "".join(map(str, cups))[1:])

    # Part 2
    # No spare 256TB of RAM nor repetitions it seems! Use another structure.
    cups_list = list(map(int, lines[0]))
    cups_list += list(range(10, 1000001))
    cups = {
        cups_list[i]: cups_list[(i + 1) % 1000000]
        for i in range(len(cups_list))
    }
    cc = cups_list[0]
    for _ in range(10000000):
        zyoooom(cups, cc)
        cc = cups[cc]
    print("Part 2:", cups[1] * cups[cups[1]])

def move(cups):
    cc = cups[0]
    pick = cups[1:4]
    d = cc - 1 or 9
    while d in pick:
        d = d - 1 if d > 1 else 9
    del cups[1:4]
    di = cups.index(d) + 1
    cups[di:di] = pick
    cups.append(cups.pop(0))

def zyoooom(cups, c):
    pick = cups[c], cups[cups[c]], cups[cups[cups[c]]]
    after_pick = cups[pick[2]]
    dest = c - 1 or 1000000
    while dest in pick:
        dest = dest - 1 if dest > 1 else 1000000
    after_dest = cups[dest]
    cups[c] = after_pick
    cups[dest] = pick[0]
    cups[pick[2]] = after_dest

if __name__ == "__main__":
    main()

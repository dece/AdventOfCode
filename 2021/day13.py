with open("input13.txt") as f:
    coords = []
    folds = []
    for line in map(str.rstrip, f):
        if "," in line:
            coords.append(tuple(map(int, line.split(","))))
        elif line and line[0] == "f":
            c, v = line.rsplit(maxsplit=1)[-1].split("=")
            folds.append((c == "x", int(v)))

for i, (is_h, v) in enumerate(folds):
    if is_h:
        coords = set(
            (x - (x - v) * 2, y) if x > v else (x, y)
            for x, y in coords
        )
    else:
        coords = set(
            (x, y - (y - v) * 2) if y > v else (x, y)
            for x, y in coords
        )
    if i == 0:
        print(len(coords))

dx = max(coords, key=lambda p: p[0])[0] + 1
dy = max(coords, key=lambda p: p[1])[1] + 1
screen = [[" "] * dx for _ in range(dy)]
for x, y in coords:
    screen[y][x] = "█"
for row in screen:
    print("".join(row))

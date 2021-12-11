with open("input11.txt") as f:
    lines = [line.rstrip() for line in f]
cells = [list(map(int, line)) for line in lines]
dim = len(cells)


def near(x, y):
    return (
        (a, b)
        for a in range(max(0, x - 1), min(x + 2, dim))
        for b in range(max(0, y - 1), min(y + 2, dim))
        if (a, b) != (x, y)
    )


def up(x, y, f):
    if (x, y) in f:
        return
    cells[x][y] += 1
    if cells[x][y] <= 9:
        return
    f.add((x, y))
    cells[x][y] = 0
    for nx, ny in near(x, y):
        up(nx, ny, f)


def step():
    flashed = set()
    for x, row in enumerate(cells):
        for y, cell in enumerate(row):
            up(x, y, flashed)
    for fx, fy in flashed:
        cells[fx][fy] = 0
    return len(flashed)


# Part 1
num_flashes = 0
for _ in range(100):
    num_flashes += step()
print(num_flashes)

# Part 2
num_steps = 100
while sum(sum(row) for row in cells) != 0:
    step()
    num_steps += 1
print(num_steps)

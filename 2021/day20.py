from operator import itemgetter as ig

with open("input20.txt") as f:
    lines = [line.rstrip() for line in f]
iea = lines[0]
data = {
    (x, y): c == "#"
    for x, line in enumerate(lines[2:])
    for y, c in enumerate(line)
}


def near(x, y):
    return ((a, b) for a in range(x - 1, x + 2) for b in range(y - 1, y + 2))


def enhance(image, unkv):
    next_image = {}
    xmin, ymin = min(image, key=ig(0))[0] - 1, min(image, key=ig(1))[1] - 1
    xmax, ymax = max(image, key=ig(0))[0] + 1, max(image, key=ig(1))[1] + 1
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            v = 0
            for nnp in near(x, y):
                v = (v << 1) | int(image.get(nnp, unkv))
            next_image[(x, y)] = iea[v] == "#"
    return next_image


def solve(num_steps):
    image = data
    for i in range(num_steps):
        image = enhance(image, i % 2 == 1)
    print(sum(image.values()))


solve(2)
solve(50)

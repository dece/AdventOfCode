with open("input17.txt") as f:
    line = f.read().rstrip()
(xmin, xmax), (ymin, ymax) = (
    tuple(map(int, part.rstrip(",")[2:].split("..")))
    for part in line.split()[2:]
)

# highest y regardless of x will be the one using the velocity that immediately
# goes to ymin after crossing the 0 axis...
print(sum(range(abs(ymin + 1) + 1)))

n = 0
ivxmax = abs(xmax)
ivymax = abs(xmax)
for ivx in range(ivxmax, -1, -1):
    for ivy in range(ivymax, -ivymax - 1, -1):
        x, y = 0, 0
        vx, vy = ivx, ivy
        while x <= xmax and y >= ymin:
            x += vx
            y += vy
            if vx > 0:
                vx -= 1
            vy -= 1
            if xmin <= x <= xmax and ymin <= y <= ymax:
                n += 1
                break
print(n)

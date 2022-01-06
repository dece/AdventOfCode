with open("input22.txt") as f:
    lines = [line.rstrip() for line in f]
steps = []
for line in lines:
    toggle, coords = line.split()
    xr, yr, zr = (
        tuple(map(int, coord[2:].split("..")))
        for coord in coords.split(",")
    )
    steps.append((toggle == "on", (xr, yr, zr)))


def print_volume(cuboids):
    num_on = sum(
        (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)
        for (x1, x2), (y1, y2), (z1, z2) in cuboids
    )
    print(num_on)


cuboids = []
for index, (toggle, step_cuboid) in enumerate(steps):
    next_cuboids = []
    (sx1, sx2), (sy1, sy2), (sz1, sz2) = step_cuboid
    for cuboid in cuboids:
        # If this cuboid does not intersect with our step, skip it.
        if not all(
            not (a1 > b2 or b1 > a2)
            for (a1, a2), (b1, b2) in zip(cuboid, step_cuboid)
        ):
            next_cuboids.append(cuboid)
            continue
        (cx1, cx2), (cy1, cy2), (cz1, cz2) = cuboid
        # Create a new sliced cube for each intersecting plane.
        # Probably cleaner to do proper cuboid intersection but pffffff
        if cx1 <= sx2 <= cx2:
            next_cuboids.append(((sx2 + 1, cx2), (cy1, cy2), (cz1, cz2)))
            cx2 = sx2
        if cx1 <= sx1 <= cx2:
            next_cuboids.append(((cx1, sx1 - 1), (cy1, cy2), (cz1, cz2)))
            cx1 = sx1
        if cy1 <= sy2 <= cy2:
            next_cuboids.append(((cx1, cx2), (sy2 + 1, cy2), (cz1, cz2)))
            cy2 = sy2
        if cy1 <= sy1 <= cy2:
            next_cuboids.append(((cx1, cx2), (cy1, sy1 - 1), (cz1, cz2)))
            cy1 = sy1
        if cz1 <= sz2 <= cz2:
            next_cuboids.append(((cx1, cx2), (cy1, cy2), (sz2 + 1, cz2)))
            cz2 = sz2
        if cz1 <= sz1 <= cz2:
            next_cuboids.append(((cx1, cx2), (cy1, cy2), (cz1, sz1 - 1)))
            cz1 = sz1
    if toggle:
        next_cuboids.append(step_cuboid)
    cuboids = next_cuboids
    if index == 19:
        print_volume(cuboids)
print_volume(cuboids)

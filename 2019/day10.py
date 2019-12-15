import math

import numpy as np


def main():
    with open("day10.txt", "rt") as input_file:
        amap = [line.rstrip() for line in input_file.readlines()]

    asteroids = []
    for y, line in enumerate(amap):
        for x, value in enumerate(line):
            if value == "#":
                asteroids.append((x, y))

    best_vis = 0
    best_pos = None
    for pos in asteroids:
        vis = num_visible_asts(asteroids, pos)
        if vis > best_vis:
            best_vis, best_pos = vis, pos
    print(f"Best visibility is {best_vis} at {best_pos}.")

def num_visible_asts(asts, ref):
    asts = asts.copy()
    asts.remove(ref)
    angles = [np.angle(np.complex(ast[0] - ref[0], ast[1] - ref[1])) for ast in asts]
    return len(set(angles))


if __name__ == "__main__":
    main()

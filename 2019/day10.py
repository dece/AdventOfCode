from collections import defaultdict
import time

import numpy as np


DIM = 40

EX = [
    ".#....#####...#..",
    "##...##.#####..##",
    "##...#...#.#####.",
    "..#.....#...###..",
    "..#.#.....#....##",
]


def main():
    with open("day10.txt", "rt") as input_file:
        amap = [line.rstrip() for line in input_file.readlines()]
        # amap = [line.rstrip() for line in EX]

    asteroids = []
    for y, line in enumerate(amap):
        for x, value in enumerate(line):
            if value == "#":
                asteroids.append((x, y))

    # Part 1
    best_vis = 0
    best_pos = None
    for pos in asteroids:
        vis = num_visible_asts(asteroids, pos)
        if vis > best_vis:
            best_vis, best_pos = vis, pos
    print(f"Best visibility is {best_vis} at {best_pos}.")

    # Part 2
    pos = best_pos
    asteroids.remove(pos)
    destroyed = 0
    angles = defaultdict(list)
    for a in asteroids:
        angle = np.angle(np.complex(a[0] - pos[0], a[1] - pos[1]), deg=True)
        angles[angle].append(a)
    current_angle = -90.0
    while asteroids:
        print(f"Laser at {pos}.")
        print(f"Current angle: {current_angle}.")
        targets = angles[current_angle]
        try:
            next_angle = min([a for a in angles.keys() if a > current_angle]) 
        except ValueError:
            next_angle = -180.0
        if not targets:
            current_angle = next_angle
            continue
        print(f"Acquired targets {targets}.")
        nearest_target = min(targets, key=lambda t: dist_idea(pos, t))
        print(f"Nearest target: {nearest_target}.")

        # Pew!
        asteroids.remove(nearest_target)
        targets.remove(nearest_target)

        destroyed += 1
        print(f"Destroyed {nearest_target} -- total of {destroyed} asteroids.")
        if destroyed == 200:
            print(f"Destroyed 200th asteroid at {nearest_target}.")
            break

        current_angle = next_angle

        draw(asteroids, pos, [nearest_target])
        time.sleep(0.2)

    print(f"Answer: {100 * nearest_target[0] + nearest_target[1]}.")

def draw(asteroids, station_pos, specials=[]):
    for y in range(DIM):
        print(str(y).zfill(2), end=" ")
        for x in range(DIM):
            if (x, y) == station_pos:
                print("@", end="")
            elif (x, y) in specials:
                print("X", end="")
            elif (x, y) in asteroids:
                print("█", end="")
            else:
                print(" ", end="")
        print()
    print("   " + "0123456789"*4)

def num_visible_asts(asteroids, ref):
    asteroids = asteroids.copy()
    asteroids.remove(ref)
    angles = [np.angle(np.complex(a[0] - ref[0], a[1] - ref[1])) for a in asteroids]
    return len(set(angles))

def dist_idea(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


if __name__ == "__main__":
    main()

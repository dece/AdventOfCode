import math


def main():
    with open("day10.txt", "rt") as input_file:
        amap = [line.rstrip() for line in input_file.readlines()]

    ast_positions = []
    for x, line in enumerate(amap):
        for y, value in enumerate(line):
            if value == "#":
                ast_positions.append((x, y))

    best_vis = 0
    for pos in ast_positions:
        best_vis = max(best_vis, num_visible_asts(ast_positions, pos))

    print("Best visibility is", best_vis)

def num_visible_asts(asts, ref):
    count = 0
    for ast in asts:
        if ast[0] == ref[0] and ast[1] == ref[1]:
            continue
        if is_visible(asts, ref, ast):
            count += 1
    return count

def is_visible(asts, ref, target):
    for ast in asts:
        if ast[0] == ref[0] and ast[1] == ref[1]:
            continue
        if ast[0] == target[0] and ast[1] == target[1]:
            continue
        if is_on_line(ref, target, ast):
            return False
    return True

def is_on_line(a, b, p):
    return math.isclose(dist(a, b), dist(a, p) + dist(b, p))

def dist(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


if __name__ == "__main__":
    main()

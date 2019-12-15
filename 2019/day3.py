from collections import defaultdict
import re


EX0 = ["R8,U5,L5,D3", "U7,R6,D4,L4"]
EX1 = ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]
EX2 = ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"]


def main():
    with open("day3.txt", "rt") as input_file:
        lines = list(input_file.readlines())
    solve(lines)

def solve(input_lines):
    wires = [(wire_id, line.strip().split(",")) for wire_id, line in enumerate(input_lines)]
    grid = compute_grid(wires)

    # Part 1
    intersections = [(x, y) for x, l in grid.items() for y, wl in l.items() if len(wl) > 1]
    print("Intersections:", intersections)
    distances = [abs(p[0]) + abs(p[1]) for p in intersections]
    print("Distances:", distances)
    print("Min distance:", min(distances))

    # Part 2
    min_steps = get_earliest_intersections(grid)
    print(f"Min steps found: {min_steps}.")

def compute_grid(wires):
    grid = defaultdict(lambda: defaultdict(list))
    for wire_id, codes in wires:
        fill_grid(wire_id, codes, grid)
    return grid

CODE_RE = re.compile(r"(\w)(\d+)")

MOVES = {
    "R": (0, +1),
    "L": (0, -1),
    "U": (+1, 0),
    "D": (-1, 0),
}

def fill_grid(wire_id, codes, grid):
    x = 0
    y = 0
    steps = 0
    for code in codes:
        match = CODE_RE.match(code)
        op, arg = match.groups()
        for _ in range(int(arg)):   
            move = MOVES[op]
            x, y = x + move[0], y + move[1]
            steps += 1
            inc_point((x, y), grid, wire_id, steps)

def inc_point(point, grid, wire_id, steps):
    x, y = point
    if wire_id not in [wid for wid, s in grid[x][y]]:
        grid[x][y].append((wire_id, steps))

def get_earliest_intersections(grid):
    min_steps = 2**64
    for line in grid.values():
        for wire_ids in line.values():
            if len(wire_ids) > 1:
                steps = sum(s for _, s in wire_ids)
                if steps < min_steps:
                    min_steps = steps
    return min_steps


if __name__ == "__main__":
    main()

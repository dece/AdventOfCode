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
    intersections = get_intersections(grid)
    # print("Intersections:", intersections)
    distances = get_manhattan_distances(intersections)
    # print("Distances:", distances)
    print("Min:", min(distances))

def compute_grid(wires):
    grid = {}
    for wire_id, codes in wires:
        fill_grid(wire_id, codes, grid)
    return grid

CODE_RE = re.compile(r"(\w)(\d+)")

def fill_grid(wire_id, codes, grid):
    x = 0
    y = 0
    for code in codes:
        match = CODE_RE.match(code)
        op, arg = match.groups()
        for _ in range(int(arg)):
            if op == "R":
                y += 1
            elif op == "L":
                y -= 1
            elif op == "U":
                x += 1
            elif op == "D":
                x -= 1
            inc_point((x, y), grid, wire_id)

def inc_point(point, grid, wire_id):
    x, y = point
    if x not in grid:
        grid[x] = {}
    if y not in grid[x]:
        grid[x][y] = [wire_id]
    elif wire_id not in grid[x][y]:
        grid[x][y].append(wire_id)

def get_intersections(grid):
    intersections = []
    for x, line in grid.items():
        for y, wire_ids in line.items():
            if len(wire_ids) > 1:
                intersections.append((x, y))
    return intersections

def get_manhattan_distances(points):
    distances = []
    for point in points:
        distances.append(manhattan_dist((0, 0), point))
    return distances

def manhattan_dist(p1, p2):
    p1x, p1y = p1
    p2x, p2y = p2
    return abs(p1x - p2x) + abs(p1y - p2y)

if __name__ == "__main__":
    main()

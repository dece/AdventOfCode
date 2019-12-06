def main():
    with open("day6.txt", "rt") as input_file:
        lines = input_file.readlines()
    entries = [tuple(line.rstrip().split(")")) for line in lines]
    orbit_map = build_map(entries)
    
    # Part 1
    num_orbits = sum(count_orbits(orbit_map, s) for s in orbit_map.keys())
    print("Num orbits:", num_orbits)

    # Part 2
    you_cursor, san_cursor = orbit_map["YOU"], orbit_map["SAN"]
    you_way, san_way = [], []
    jumps = 0
    while you_cursor is not None or san_cursor is not None:
        you_cursor = orbit_map.get(you_cursor)
        san_cursor = orbit_map.get(san_cursor)
        you_way.append(you_cursor)
        san_way.append(san_cursor)
        if you_cursor in san_way:
            jumps = san_way.index(you_cursor) + len(you_way)
            break
        if san_cursor in you_way:
            jumps = you_way.index(san_cursor) + len(san_way)
            break
    print("Required jumps:", jumps + 1)

def build_map(entries):
    orbit_map = {}
    for center, satellite in entries:
        orbit_map[satellite] = center
    return orbit_map

def count_orbits(orbit_map, satellite):
    if satellite in orbit_map:
        return 1 + count_orbits(orbit_map, orbit_map[satellite])
    else:
        return 0


if __name__ == "__main__":
    main()

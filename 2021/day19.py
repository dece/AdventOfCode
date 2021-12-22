from collections import defaultdict
from itertools import combinations, permutations

with open("input19.txt") as f:
    lines = [line.rstrip() for line in f]
scanners = []
for line in lines:
    if line.startswith("--"):
        scanner_id = int(line.split()[2])
        positions = []
    elif line:
        positions.append(tuple(map(int, line.split(","))))
    else:
        scanners.append((scanner_id, positions))
scanners.append((scanner_id, positions))


def N(x, y, z): return x, y, z
def X(x, y, z): return x, -z, y
def Y(x, y, z): return -z, y, x
def add(v1, v2): return v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]
def sub(v1, v2): return v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]


orientations = [
    "N", "X", "Y", "XX", "XY", "YX", "YY", "XXX", "XXY", "XYX", "XYY", "YXX",
    "YYX", "YYY", "XXXY", "XXYX", "XXYY", "XYXX", "XYYY", "YXXX", "YYYX",
    "XXXYX", "XYXXX", "XYYYX"
]
rotations = {k: globals()[k] for k in "NXY"}


def orient(x, y, z, orientation):
    for axis in orientation:
        x, y, z = rotations[axis[::-1]](x, y, z)
    return x, y, z


overlaps = {}
oriented = {
    sb_id: [(o, [orient(*pos, o) for pos in sb]) for o in orientations]
    for sb_id, sb in scanners
}
# Using permutations is slower than combinations but it's simpler to find the
# transform path after.
for (sa_id, sa), (sb_id, _) in permutations(scanners, 2):
    for orientation, osb in oriented[sb_id]:
        diffs = defaultdict(int)
        for ax, ay, az in sa:
            for bx, by, bz in osb:
                diff = (ax - bx, ay - by, az - bz)
                diffs[diff] += 1
                if diffs[diff] >= 12:
                    overlaps[(sa_id, sb_id)] = (orientation, diff)
                    break
            else:
                continue
            break
        else:
            continue
        break


def find_transform_to_0(from_s):
    chains = [[p] for p in overlaps if p[0] == from_s]
    seen = set()
    while chains:
        chain = chains.pop(0)
        if chain[-1][1] == 0:
            return chain
        for p in overlaps:
            if p[0] == chain[-1][1] and p not in seen:
                seen.add(p)
                chains.append(chain + [p])


def see_as_0(x, y, z, sid):
    for t in find_transform_to_0(sid):
        ori, move = overlaps[t[::-1]]
        x, y, z = add(orient(x, y, z, ori), move)
    return x, y, z


def see_scanner_as_0(sid, sdata):
    for x, y, z in sdata:
        yield see_as_0(x, y, z, sid)


beacons = set()
for scanner_id in range(len(scanners)):
    beacons |= set(list(see_scanner_as_0(*scanners[scanner_id])))
print(len(beacons))
scanner_positions = [see_as_0(0, 0, 0, sid) for sid in range(len(scanners))]
print(max(
    sum(map(abs, sub(spb, spa)))
    for spa, spb in combinations(scanner_positions, 2)
))

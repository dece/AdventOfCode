from collections import defaultdict
from string import ascii_lowercase

with open("input12.txt") as f:
    lines = [line.rstrip() for line in f]
cxs = defaultdict(list)
for a, b in map(lambda s: s.split("-"), lines):
    cxs[a].append(b)
    cxs[b].append(a)


def walk(path, skip_f):
    if path[-1] == "end":
        return [path]
    valid_paths = []
    for cave in filter(lambda c: c != "start", cxs[path[-1]]):
        if skip_f(cave, path):
            continue
        valid_paths += walk(path + [cave], skip_f)
    return valid_paths


def skip1(cave, path):
    return cave[0] in ascii_lowercase and cave in path


def skip2(cave, path):
    return (
        skip1(cave, path)
        and any(
            path.count(c) > 1
            for c in filter(lambda c: c[0] in ascii_lowercase, path)
        )
    )


print(len(walk(["start"], skip1)))
print(len(walk(["start"], skip2)))

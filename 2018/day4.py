import re
from collections import defaultdict
from datetime import datetime


def main():
    with open("day4.txt", "rt") as f:
        lines = [line.rstrip() for line in f.readlines()]
    entries = [parse_entry(line) for line in lines]
    entries = sorted(entries, key=lambda e: e[0])

    sleepz = defaultdict(int)
    noight = defaultdict(lambda: [0] * 60)
    for t, v in entries:
        if not isinstance(v, bool):
            guard = v
        elif v == False:
            sleep_t = t
        elif v == True:
            sleep_d = t - sleep_t
            sleep_minutes = sleep_d.seconds // 60
            sleepz[guard] += sleep_minutes
            for i in range(sleep_minutes):
                noight[guard][sleep_t.minute + i] += 1
    lazy_g = max(sleepz, key=lambda k: sleepz[k])
    print("Laziest guard:", lazy_g)
    sleepiest_min = max(range(60), key=lambda m: noight[lazy_g][m])
    print("Sleepiest minute:", sleepiest_min)
    print("Part 1:", lazy_g * sleepiest_min)

    reliable_v = -1
    for g in noight:
        sleepiest_min = max(range(60), key=lambda m: noight[g][m])
        sleepiest_v = noight[g][sleepiest_min]
        if sleepiest_v > reliable_v:
            reliable_g = g
            reliable_m = sleepiest_min
            reliable_v = sleepiest_v
    print("Part 2:", reliable_g * reliable_m)


LINE_RE = re.compile(r"^\[([^\]]+)\] (.+)$")

def parse_entry(line):
    match = LINE_RE.match(line)
    ts, content = match.groups()
    dt = datetime.fromisoformat(ts)
    if content.startswith("Guard"):
        v = int(content.split()[1][1:])
    elif content.startswith("w"):
        v = True
    elif content.startswith("f"):
        v = False
    return (dt, v)


if __name__ == "__main__":
    main()

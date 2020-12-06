#!/usr/bin/env python3

import os
from datetime import date

TEMPLATE = """\
def main():
    with open("{}", "rt") as f:
        lines = [line.rstrip() for line in f.readlines()]


if __name__ == "__main__":
    main()
"""

day = date.today().day
with open(f"day{day}.py", "wt") as f:
    f.write(TEMPLATE.format(f"day{day}.txt"))
os.system(f"python ../fetch.py {day}")

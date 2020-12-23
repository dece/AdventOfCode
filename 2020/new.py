#!/usr/bin/env python3

import os
from datetime import date

TEMPLATE = """\
import sys

def main():
    lines = [line.rstrip() for line in sys.stdin]

if __name__ == "__main__":
    main()
"""

day = date.today().day
with open(f"day{day}.py", "wt") as f:
    f.write(TEMPLATE)
os.system(f"python ../fetch.py {day}")

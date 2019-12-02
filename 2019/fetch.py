import os
import requests
import sys

if len(sys.argv) != 2:
    print("Usage: <fetch> day")
    sys.exit()
day = sys.argv[1]

URL = "https://adventofcode.com/2019/day/{}/input"
SESSION_ID = os.environ["AOC_SESSION"]

response = requests.get(URL.format(day), cookies={"session": SESSION_ID})
response.raise_for_status()

with open("day{}.txt".format(day), "wt") as output_file:
    output_file.write(response.text)

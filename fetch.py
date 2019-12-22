from datetime import datetime
import os
import requests
import sys

if len(sys.argv) < 2:
    print("Usage: <fetch> day")
    sys.exit()
day = sys.argv[1]
year = sys.argv[2] if len(sys.argv) > 2 else str(datetime.now().year)

URL = "https://adventofcode.com/{}/day/{}/input"
SESSION_ID = os.environ["AOC_SESSION"]

response = requests.get(URL.format(year, day), cookies={"session": SESSION_ID})
response.raise_for_status()

with open("day{}.txt".format(day), "wt") as output_file:
    output_file.write(response.text)

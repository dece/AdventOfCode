#!/usr/bin/env python3
import argparse
import os
import webbrowser
from datetime import datetime
from pathlib import Path

import requests


URL = "https://adventofcode.com/{}/day/{}"
SESSION_ID = os.environ["AOC_SESSION"]


now = datetime.now()
parser = argparse.ArgumentParser()
parser.add_argument("day", type=int, default=now.day)
parser.add_argument("year", type=int, default=now.year)
parser.add_argument("--lang", default="py")
args = parser.parse_args()
day, year, lang = args.day, args.year, args.lang

day_url = URL.format(year, day)
input_url = day_url + "/input"
response = requests.get(input_url, cookies={"session": SESSION_ID})
response.raise_for_status()
input_text = response.text
root_dir = Path(__file__).parent.resolve()
year_dir = root_dir / str(year)
year_dir.mkdir(exist_ok=True)
input_path = year_dir / f"input{day}.txt"
with open(input_path, "wt") as output_file:
    output_file.write(input_text)

template_path = root_dir / f"template.{lang}"
if template_path.exists():
    if lang == "rs":
        bin_path = year_dir / "src" / "bin"
        bin_path.mkdir(exist_ok=True)
        script_path = bin_path / f"day{day}.{lang}"
    else:
        script_path = year_dir / f"day{day}.{lang}"
    with open(template_path, "rt") as template_file:
        template = template_file.read()
    template = template.format(day=day)
    with open(script_path, "wt") as script_file:
        script_file.write(template)
else:
    print(f"No template for {lang}.")

webbrowser.open_new_tab(day_url)

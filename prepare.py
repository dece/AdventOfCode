import argparse
import os
import shutil
import webbrowser
from datetime import datetime
from pathlib import Path

import requests


URL = "https://adventofcode.com/{}/day/{}"
SESSION_ID = os.environ["AOC_SESSION"]


def main():
    now = datetime.now()
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int, default=now.day)
    parser.add_argument("year", type=int, default=now.year)
    parser.add_argument("--lang", default="py")
    args = parser.parse_args()

    day_url = get_url(args.day, args.year)
    input_url = day_url + "/input"
    input_text = fetch(input_url)
    create_files(input_text, args.day, args.year, args.lang)
    webbrowser.open_new_tab(day_url)
    webbrowser.open_new_tab(input_url)

def fetch(input_url):
    response = requests.get(input_url, cookies={"session": SESSION_ID})
    response.raise_for_status()
    return response.text

def get_url(day, year):
    return URL.format(year, day) 

def create_files(text, day, year, lang):
    root_dir = Path(__file__).parent.resolve()
    year_dir = root_dir / str(year)
    year_dir.mkdir(exist_ok=True)
    input_path = year_dir / f"day{day}.txt"
    with open(input_path, "wt") as output_file:
        output_file.write(text)
    template_path = root_dir / f"template.{lang}"
    if template_path.exists():
        if lang == "rs":
            bin_path = year_dir / "src" / "bin"
            bin_path.mkdir(exist_ok=True)
            script_path = bin_path / f"day{day}.{lang}"
        else:
            script_path = year_dir / f"day{day}.{lang}"
        shutil.copyfile(template_path, script_path)
    else:
        print(f"No template for {lang}.")


if __name__ == "__main__":
    main()

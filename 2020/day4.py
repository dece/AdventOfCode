import re
import string


REQ = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]


def main():
    with open("day4.txt", "rt") as f:
        lines = [line.rstrip() for line in f.readlines()]
    passports = get_passports(lines)

    # Part 1
    num_valids = 0
    for passport in passports:
        if all(k in passport for k in REQ):
            num_valids += 1
    print("Valids:", num_valids)

    # Part 2
    num_valids = 0
    hair_re = re.compile(r"#[abcdef\d]{6}")
    for passport in passports:
        if not all(k in passport for k in REQ):
            continue
        if not (1920 <= int(passport["byr"]) <= 2002):
            continue
        if not (2010 <= int(passport["iyr"]) <= 2020):
            continue
        if not (2020 <= int(passport["eyr"]) <= 2030):
            continue
        if not (
            (passport["hgt"].endswith("cm") and 150 <= int(passport["hgt"][:-2]) <= 193)
            or (passport["hgt"].endswith("in") and 59 <= int(passport["hgt"][:-2]) <= 76)
        ):
            continue
        if not hair_re.match(passport["hcl"]):
            continue
        if not passport["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            continue
        if not (len(passport["pid"]) == 9 and all(c in string.digits for c in passport["pid"])):
            continue
        num_valids += 1
    print("P2 valids:", num_valids)


def get_passports(lines):
    passports = []
    passport = {}
    for line in lines:
        elements = line.split()
        for element in elements:
            k, v = element.split(":")
            passport[k] = v
        if not line:
            passports.append(passport)
            passport = {}
    passports.append(passport)
    return passports


if __name__ == "__main__":
    main()

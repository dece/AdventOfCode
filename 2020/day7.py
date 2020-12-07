import re
from collections import defaultdict


LINE_RE = re.compile(r"^(\w+ \w+) bags contain (.+)\.$")
CONT_RE = re.compile(r"(\d+) (\w+ \w+) bags?")


def main():
    with open("day7.txt", "rt") as f:
        lines = [line.rstrip() for line in f.readlines()]
    rules = defaultdict(dict)
    for line in lines:
        match = LINE_RE.match(line)
        subject, contained = match.groups()
        contained = contained.split(", ")
        for c in contained:
            match = CONT_RE.match(c)
            if match:
                cn, ct = match.groups()
                rules[subject][ct] = int(cn)

    # Part 1
    num_containers = sum(contain_shiny_gold(bag, rules) for bag in rules.copy())
    print("Containing at least 1 shiny gold:", num_containers)

    # Part 2
    inside_shiny_gold = count_bags("shiny gold", rules) - 1
    print("Inside shiny gold:", inside_shiny_gold)


def contain_shiny_gold(bag, rules):
    if "shiny gold" in rules[bag]:
        return True
    return any(contain_shiny_gold(b, rules) for b in rules[bag])


def count_bags(bag, rules):
    return sum(count_bags(b, rules) * rules[bag][b] for b in rules[bag]) + 1


if __name__ == "__main__":
    main()

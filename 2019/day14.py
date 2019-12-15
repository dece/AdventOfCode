import math
import re


def main():
    with open("day14.txt", "rt") as input_file:
        lines = [line.rstrip() for line in input_file.readlines()]
    line_re = re.compile(r"(.+) => (.+)")
    raw_transmos = [line_re.match(line).groups() for line in lines]
    transmos = {}
    for inputs, outputs in raw_transmos:
        mult, result = outputs.split(" ")
        input_comps = [i.split(" ") for i in inputs.split(", ")]
        input_tuples = [(int(q), n) for q, n in input_comps]
        transmos[result] = int(mult), input_tuples

    # Part 1
    ore_per_full = get_required_ore(transmos, "FUEL", 1, {})
    print("Required ore for 1 FUEL:", ore_per_full)

    # Part 2
    # Input gives 397771 OPF.
    # 10^12 ores with 13312 OPF example gives 82892753 FUEL.
    # 10^12 ores with 180697 OPF example gives 5586022 FUEL.
    # 10^12 ores with 2210736 OPF example gives 460664 FUEL.
    # 10^12 / 82892753 / 13312 ~= 0.91
    # 10^12 / 5586022 / 180697 ~= 0.99
    # 10^12 / 460664 / 2210736 ~= 0.98
    # Let's say our reaction will have this value at about 0.985.
    # 10^12 / x / 397771 = 0.985  ->  x = 2552294
    # Now on to our search.

    fuel = 2552294
    cursor = 10000
    last_result = 0
    min_target = 10**12 - ore_per_full
    max_target = 10**12
    was_below = False
    was_above = False
    while last_result not in range(min_target, max_target):
        last_result = get_required_ore(transmos, "FUEL", fuel, {})
        print("{} FUEL requires {} ORE.".format(fuel, last_result))
        if last_result < min_target:
            if was_above:
                cursor /= 2
            fuel += cursor
        elif last_result > max_target:
            if was_below:
                cursor /= 2
            fuel -= cursor
    
def get_required_ore(transmos, name, quantity, leftovers):
    if name == "ORE":
        return quantity

    mult, comps = transmos[name]
    num_reactions = math.ceil(quantity / mult)

    created = 0
    if name in leftovers:
        created += leftovers[name]
        leftovers[name] = 0

    req_ore = 0
    for _ in range(num_reactions):
        if created >= quantity:
            break
        req_ore += sum(get_required_ore(transmos, rn, rq, leftovers) for rq, rn in comps)
        created += mult

    if created > quantity:
        leftover = created - quantity
        leftovers[name] = leftovers.get(name, 0) + leftover
    
    return req_ore


if __name__ == "__main__":
    main()

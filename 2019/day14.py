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

    print("Required ore for 1 FUEL:", get_required_ore(transmos, "FUEL", 1, {}))
    
def get_required_ore(transmos, name, quantity, rabs):
    if name == "ORE":
        return quantity

    print("What is required for {} {}?".format(quantity, name))
    mult, comps = transmos[name]
    num_reactions = math.ceil(quantity / mult)

    created = 0
    if name in rabs:
        print("  Found {} in rab.".format(rabs[name]))
        created += rabs[name]
        rabs[name] = 0

    req_ore = 0
    for _ in range(num_reactions):
        if created >= quantity:
            break
        print("  Creation of {} {}...".format(mult, name))
        for rq, rn in comps:
            req_ore += get_required_ore(transmos, rn, rq, rabs)
        created += mult
    print("  Possessing {} {}.".format(created, name))

    if created > quantity:
        leftover = created - quantity
        rabs[name] = rabs.get(name, 0) + leftover
        print("  Stored {} {} in rab.".format(leftover, name))
    
    print("Answer ({} {}): {} ores".format(quantity, name, req_ore))
    return req_ore


if __name__ == "__main__":
    main()

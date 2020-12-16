import sys
from collections import defaultdict
from functools import reduce
from itertools import permutations


def main():
    lines = [line.rstrip() for line in sys.stdin]

    step = 0
    rules = {}
    nearby = []
    for line in lines:
        if not line:
            step += 1
            continue
        if step == 0:
            name, ranges = line.split(": ")
            rules[name] = tuple(map(
                lambda rs: tuple(map(int, rs.split("-"))),
                [rs for rs in ranges.split(" or ")]
            ))
        elif step == 1 and not line.startswith("your"):
            your_ticket = list(map(int, line.split(",")))
            ticket_len = len(your_ticket)
        elif step == 2 and not line.startswith("nearby"):
            nearby.append(list(map(int, line.split(","))))

    # Part 1
    acc = 0
    invalids = []
    for nt in nearby:
        for n in nt:
            for rule in rules.values():
                if n_sat_rule(n, rule):
                    break
            else:  # satisfies no rules
                invalids.append(nt)
                acc += n
    print("Part 1:", acc)

    # Part 2
    tickets = [your_ticket, *filter(lambda t: t not in invalids, nearby)]
    isat = {}
    for i in range(ticket_len):
        possible_rules = set(rules.keys())
        for ticket in tickets:
            n = ticket[i]
            for rname, r in rules.items():
                if not n_sat_rule(n, r):
                    possible_rules.remove(rname)
        isat[i] = possible_rules
    # for some reason, len(s) for s in isat.values() is unique per i, which
    # means we could easily solve the whole field attribution incrementally!
    solved_fields = set()
    field_map = {}
    for i, s in sorted(isat.items(), key=lambda item: len(item[1])):
        s -= solved_fields
        assert len(s) == 1
        f = s.pop()
        field_map[i] = f
        solved_fields.add(f)
    dep_fields = [i for i, f in field_map.items() if f.startswith("departure")]
    your_ticket_values = [your_ticket[i] for i in dep_fields]
    print("Part 2:", reduce(lambda a, b: a * b, your_ticket_values, 1))


def n_sat_rule(n, r):
    return r[0][0] <= n <= r[0][1] or r[1][0] <= n <= r[1][1]


if __name__ == "__main__":
    main()

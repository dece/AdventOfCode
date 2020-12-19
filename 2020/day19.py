import re
import sys


rules, frules, messages = {}, {}, []
srules = {}


def main():
    lines = [line.rstrip() for line in sys.stdin]
    step = 0
    for line in lines:
        if not line:
            step += 1
            continue
        if step == 0:
            rid, rcontent = line.split(": ")
            if '"' in rcontent:
                frules[int(rid)] = rcontent.strip('"')
            else:
                rules[int(rid)] = tuple(map(
                    lambda seq: tuple(map(int, seq.split())),
                    rcontent.split(" | ")
                ))
        else:
            messages.append(line)

    # Part 1
    rule_0 = re.compile("^" + get_regex(0) + "$")
    valids = list(filter(lambda m: rule_0.match(m) is not None, messages))
    print("Num valids:", len(valids))

    # Part 2
    del rules[8]
    rule_42 = get_regex(42)
    srules[8] = rule_42 + "+"
    del rules[11]
    rule_31 = get_regex(31)
    srules[11] = "(" + "|".join(
        f"{rule_42}{{{i}}}{rule_31}{{{i}}}"
        for i in range(1, 10)  # haha
    ) + ")"
    rule_0 = re.compile("^" + get_regex(0) + "$")
    valids = list(filter(lambda m: rule_0.match(m) is not None, messages))
    print("Num valids with fake loop:", len(valids))


def get_regex(rule_id):
    if (char := frules.get(rule_id)):
        return char
    if (regex := srules.get(rule_id)):
        return regex
    seq_res = []
    for seq in rules[rule_id]:
        seq_res.append("".join(get_regex(r) for r in seq))
    return f"({'|'.join(seq_res)})"
        

if __name__ == "__main__":
    main()

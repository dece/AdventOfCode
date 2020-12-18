import re
import sys


SUBEXPR = re.compile(r"\([^\(\)]+\)")


def main():
    lines = [line.rstrip() for line in sys.stdin]

    # Part 1
    acc = 0
    for line in lines:
        while (subexprs := list(SUBEXPR.finditer(line))):
            for sub in subexprs:
                sub_text = sub.group(0)
                value = spacemath(sub_text.strip("()").split())
                line = line.replace(sub_text, str(value), 1)
        acc += spacemath(line.split())
    print("Sum:", acc)

    # Part 2
    acc = 0
    for line in lines:
        while (subexprs := list(SUBEXPR.finditer(line))):
            for sub in subexprs:
                sub_text = sub.group(0)
                value = advanced(sub_text.strip("()").split())
                line = line.replace(sub_text, str(value), 1)
        acc += advanced(line.split())
    print("Sum with advanced math:", acc)


def spacemath(tokens):
    acc = int(tokens[0])
    for i in range(1, len(tokens) - 1, 2):
        op, rhs = tokens[i], tokens[i + 1]
        acc = (acc + int(rhs)) if op == "+" else (acc * int(rhs))
    return acc


def advanced(tokens):
    while len(tokens) > 1:  # solve additions first
        try:
            i = tokens.index("+")
        except ValueError:
            break
        simplification = int(tokens[i - 1]) + int(tokens[i + 1])
        tokens[i - 1:i + 2] = [simplification]
    return spacemath(tokens)  # lazily reuse spacemath for multiplication


if __name__ == "__main__":
    main()

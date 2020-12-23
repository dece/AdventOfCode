import re
import sys
from functools import reduce

LINE_RE = re.compile(r"(.+) \(contains (.+)\)")

def main():
    lines = [line.rstrip() for line in sys.stdin]
    foods = []
    for line in lines:
        i, a = LINE_RE.match(line).groups()
        foods.append((set(i.split()), set(a.split(", "))))
    ingredients = set(i for il, _ in foods for i in il)
    allergens = set(a for _, al in foods for a in al)

    # Part 1
    matches = {}
    while len(matches) < len(allergens):
        for allergen in allergens:
            p_ings = [
                set(filter(lambda i: i not in matches, f[0]))
                for f in foods if allergen in f[1]
            ]
            c_ings = reduce(lambda a, b: a & b, p_ings, ingredients)
            if len(c_ings) == 1:
                i = c_ings.pop()
                matches[i] = allergen
    clean_ings = ingredients.difference(set(matches.keys()))
    num_appearances = sum(
        ci in fis
        for fis, _ in foods
        for ci in clean_ings
    )
    print(f"Clean ingredients appear {num_appearances} times.")

    # Part 2
    canonical = ",".join(
        f for f, a in sorted(matches.items(), key=lambda m: m[1])
    )
    print("Canonical list:", canonical)

if __name__ == "__main__":
    main()

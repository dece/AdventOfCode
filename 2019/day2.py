import itertools

from intcode import Intcode


def main():
    with open("day2.txt", "rt") as input_file:
        text = input_file.readlines()[0].rstrip()
    codes = Intcode.parse_input(text)

    # Part 1
    codes_p1 = codes.copy()
    codes_p1[1] = 12
    codes_p1[2] = 2
    ic = Intcode(codes_p1)
    ic.run()
    print(f"Value at pos 0: {ic._memory[0]}.")

    # Part 2
    noun, verb = 0, 0
    for x, y in itertools.permutations(range(1, 100), 2):
        codes_p2 = codes.copy()
        codes_p2[1] = x
        codes_p2[2] = y
        ic = Intcode(codes_p2)
        ic.run()
        if ic._memory[0] == 19690720:
            noun, verb = x, y
            break
    print(f"Found noun={noun} and verb={verb}.")
    print(f"Answer: {100 * noun + verb}")


if __name__ == "__main__":
    main()

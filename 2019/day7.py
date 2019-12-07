import itertools

from intcode import Intcode


def main():
    with open("day7.txt", "rt") as input_file:
        first_line = input_file.readlines()[0]
    codes = Intcode.parse_input(first_line)

    phase_settings_perm = itertools.permutations(range(5), 5)
    max_output = 0
    for phases in phase_settings_perm:
        inout = 0
        for amp_id in range(5):
            inout = Intcode(codes).run([phases[amp_id], inout])
        max_output = max(max_output, inout)
    print("Max output:", max_output)


if __name__ == "__main__":
    main()

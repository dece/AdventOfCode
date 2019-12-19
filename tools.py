from intcode import Intcode


def parse_intcode(filename):
    with open(filename, "rt") as input_file:
        return Intcode.parse_input(input_file.read().rstrip())

from intcode import Intcode


EX1 = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
EX2 = "1102,34915192,34915192,7,4,7,99,0"
EX3 = "104,1125899906842624,99"


def main():
    with open("day9.txt", "rt") as input_file:
        text = input_file.readlines()[0].rstrip()
    codes = Intcode.parse_input(text)

    # Part 1
    Intcode(codes, print_output=True).run([1])

    # Part 2
    Intcode(codes, print_output=True).run([2])


if __name__ == "__main__":
    main()

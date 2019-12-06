from enum import IntEnum
import sys

def main():
    with open("day5.txt", "rt") as input_file:
        codes = [int(i) for i in input_file.read().strip().split(",")]
    last_output = run_intcode(codes)
    print("Last output:", last_output)

class Opcode(IntEnum):
    ADD = 1
    MUL = 2
    IN = 3
    OUT = 4
    HALT = 99

class ParamMode(IntEnum):
    POS = 0
    IMM = 1

def run_intcode(codes):
    fixed_input = 1
    last_output = 0
    ip = 0
    while True:
        code, modes = parse_code(codes[ip])
        mode1, mode2, mode3 = modes
        if code == Opcode.ADD:
            print("ADD:", codes[ip : ip + 4])
            operand1 = resolve_param(codes, ip + 1, mode1)
            operand2 = resolve_param(codes, ip + 2, mode2)
            output_pos = codes[ip + 3]
            codes[output_pos] = operand1 + operand2
            ip += 4
        elif code == Opcode.MUL:
            print("MUL:", codes[ip : ip + 4])
            operand1 = resolve_param(codes, ip + 1, mode1)
            operand2 = resolve_param(codes, ip + 2, mode2)
            output_pos = codes[ip + 3]
            codes[output_pos] = operand1 * operand2
            ip += 4
        elif code == Opcode.IN:
            print("IN:", codes[ip : ip + 2])
            operand_pos = codes[ip + 1]
            codes[operand_pos] = fixed_input
            ip += 2
        elif code == Opcode.OUT:
            print("OUT:", codes[ip : ip + 2])
            operand_pos = codes[ip + 1]
            last_output = codes[operand_pos]
            print("\t->", last_output)
            ip += 2
        elif code == Opcode.HALT:
            print("HALT.")
            break
        else:
            sys.exit("Wrong opcode: {}".format(code))
    return last_output

def parse_code(code):
    opcode = get_digit(code, 2)*10 + get_digit(code, 1)
    if code < 100:
        return opcode, (ParamMode.IMM,) * 3
    mode1 = ParamMode(get_digit(code, 3))
    mode2 = ParamMode(get_digit(code, 4))
    mode3 = ParamMode(get_digit(code, 5))
    return opcode, (mode1, mode2, mode3)

def get_digit(value, digit):
    digit_str = str(value)
    if digit > len(digit_str):
        return 0
    try:
        return int(digit_str[len(digit_str) - digit])
    except IndexError:
        return 0

def resolve_param(codes, pos, mode):
    if mode == ParamMode.POS:
        return codes[codes[pos]]
    elif mode == ParamMode.IMM:
        return codes[pos]


if __name__ == "__main__":
    main()

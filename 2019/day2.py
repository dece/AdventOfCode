import sys

CODES = None
with open("day2.txt", "rt") as input_file:
    CODES = [int(i) for i in input_file.read().strip().split(",")]

CODES[1] = 12
CODES[2] = 2

ip = 0
while True:
    code = CODES[ip]
    if code == 1:
        operand1_pos = CODES[ip + 1]
        operand2_pos = CODES[ip + 2]
        output_pos = CODES[ip + 3]
        CODES[output_pos] = CODES[operand1_pos] + CODES[operand2_pos]
        ip += 4
    elif code == 2:
        operand1_pos = CODES[ip + 1]
        operand2_pos = CODES[ip + 2]
        output_pos = CODES[ip + 3]
        CODES[output_pos] = CODES[operand1_pos] * CODES[operand2_pos]
        ip += 4
    elif code == 99:
        break
    else:
        print("Wrong opcode:", code)
        sys.exit()

print("Value at pos0:", CODES[0])

import math
import sys


def main():
    with open("day16.txt", "rt") as input_file:
        inputs = [int(i) for i in input_file.read().rstrip()]

    # Part 1
    result = phaze2phaze(inputs)
    print(f"First 8 digits: {''.join(str(int(i)) for i in result[:8])}")

    # Part 2
    offset = int(''.join(str(i) for i in inputs[:7]))
    rev_inputs = [i for _ in range(10000) for i in reversed(inputs)]
    rev_offset = len(rev_inputs) - offset

    print(f"Offset: {offset}. Reversed offset: {rev_offset}")
    result = phaze4phaze(rev_inputs, index_limit=rev_offset + 8)
    result_slice = result[rev_offset-8:rev_offset]
    result_slice.reverse()
    print(f"Answer: {''.join(str(int(i)) for i in result_slice)}")

def p(index, pos):
    return round(math.cos(((pos - index + 1) // index) * (math.pi / 2)))

def phaze2phaze(inputs, rounds=100):
    """ https://www.youtube.com/watch?v=i0leFvyLEF8 """
    for phase_id in range(rounds):
        print_phaze(phase_id + 1)
        outputs = [None] * len(inputs)
        for index in range(len(inputs)):
            out = sum(x * p(index + 1, pos + index) for pos, x in enumerate(inputs[index:]))
            outputs[index] = abs(math.fmod(out, 10))
        inputs = outputs
    return inputs

def phaze4phaze(rev_inputs, index_limit):
    for phase_id in range(100):
        print_phaze(phase_id + 1)
        outputs = [None] * index_limit
        sumsum = 0
        for index in range(index_limit):
            sumsum += rev_inputs[index]
            outputs[index] = abs(math.fmod(sumsum, 10))
        rev_inputs = outputs
    return rev_inputs

def print_phaze(n):
    print(f"{n}... ", end="")
    sys.stdout.flush()


if __name__ == "__main__":
    main()

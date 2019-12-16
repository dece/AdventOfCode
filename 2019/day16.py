import math


def main():
    with open("day16.txt", "rt") as input_file:
        inputs = [int(i) for i in input_file.read().rstrip()]
        # inputs = [1,2,3,4,5,6,7,8]
        # inputs = [0,3,0,3,6,7,3,2,5,7,7,2,1,2,9,4,4,0,6,3,4,9,1,5,6,5,4,7,4,6,6,4]

    # Part 1
    result = phaze2phaze(inputs)
    print(f"First 8 digits: {''.join(str(int(i)) for i in result[:8])}")

    # Part 2
    # offset = int(''.join(str(i) for i in inputs[:7]))
    # rev_inputs = [i for _ in range(10000) for i in reversed(inputs)]
    # rev_offset = len(rev_inputs) - offset

    # print(f"Offset: {offset}. Reversed offset: {rev_offset}")
    # result = phaze2phaze(rev_inputs, index_limit=rev_offset)
    # result_slice = result[rev_offset - 8:rev_offset]
    # assert result_slice == [8,4,4,6,2,0,2,6]
    # print(f"8 digits at offset: {''.join(str(int(i)) for i in result_slice)}")

def p(index, pos):
    return round(math.cos(((pos - index + 1) // index) * (math.pi / 2)))

def phaze2phaze(inputs, rounds=100, index_limit=None):
    """ https://www.youtube.com/watch?v=i0leFvyLEF8 """
    for phase_id in range(rounds):
        phase_id += 1
        outputs = [None] * len(inputs)
        print(f"Phase {phase_id}... ")
        for index in range(index_limit or len(inputs)):
            out = sum(x * p(index + 1, pos + index) for pos, x in enumerate(inputs[index:]))
            outputs[index] = abs(math.fmod(out, 10))
        inputs = outputs
    return inputs


if __name__ == "__main__":
    main()

import math


def main():
    with open("day16.txt", "rt") as input_file:
        inputs = [int(i) for i in input_file.read().rstrip()]
    inputs_orig = inputs.copy()

    # result = phaze2phaze(inputs)
    # print(f"First 8 digits: {''.join(str(int(i)) for i in result[:8])}")

    # Part 2
    offset = int(''.join(str(i) for i in inputs[:7]))
    inputs = [i for _ in range(10000) for i in inputs_orig]
    result = phaze2phaze(inputs)
    print(f"8 digits at offset: {''.join(str(int(i)) for i in result[offset:offset + 8])}")


def phaze2phaze(inputs):
    p = [0, 1, 0, -1]
    for phase_id in range(100):
        phase_id += 1
        print(f"Phase {phase_id}...")
        outputs = [None] * len(inputs)
        for index in range(len(inputs)):
            ex_f = index + 1
            ex_p = [p[i // ex_f] for i in range(len(p) * ex_f)]
            while len(ex_p) < len(inputs) + 1:
                ex_p += ex_p  # yikes
            ex_p = ex_p[1:len(inputs) + 1]
            out = sum(a * b for a, b in zip(inputs, ex_p))
            outputs[index] = abs(math.fmod(out, 10))
        inputs = outputs
    return inputs


if __name__ == "__main__":
    main()


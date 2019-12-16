import math


def main():
    with open("day16.txt", "rt") as input_file:
        inputs = [int(i) for i in input_file.read().rstrip()]

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
    print(f"First 8 digits: {''.join(str(int(i)) for i in inputs[:8])}")


if __name__ == "__main__":
    main()


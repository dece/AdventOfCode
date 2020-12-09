import itertools


def main():
    with open("day9.txt", "rt") as f:
        series = [int(line.rstrip()) for line in f.readlines()]
    
    # Part 1
    frame_len = 25
    for i in range(len(series) - frame_len):
        frame = series[i : i + frame_len]
        n = series[i + frame_len]
        for a, b in itertools.combinations(frame, 2):
            if a + b == n:
                break
        else:
            print("Invalid N:", n)
            break

    # Part 2
    for i in range(len(series)):  # what is indexerror when you know it breaks
        for j in range(1, len(series)):
            frame = series[i : i + j + 1]
            if (s := sum(frame)) == n:
                print("Answer:", min(frame) + max(frame))
                return
            elif s > n:
                break


if __name__ == "__main__":
    main()

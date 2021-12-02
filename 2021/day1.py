import sys


def main():
    lines = [line.rstrip() for line in sys.stdin]

    # Part 1
    nums = map(int, lines)
    prev = 99999
    incs = 0
    for n in nums:
        if n > prev:
            incs += 1
        prev = n
    print(incs)

    # Part 2
    nums = list(map(int, lines))
    prev = 99999
    incs = 0
    for i in range(2, len(nums)):
        sus = nums[i] + nums[i - 1] + nums[i - 2]
        if sus > prev:
            incs += 1
        prev = sus
    print(incs)


if __name__ == "__main__":
    main()

import re
import sys
from itertools import combinations_with_replacement


def main():
    lines = [line.rstrip() for line in sys.stdin]

    # Part 1
    int_len = 36
    meme = {}
    mem_re = re.compile(r"mem\[(\d+)\] = (\d+)")
    for line in lines:
        if line.startswith("mask"):
            mask_str = line.split("=")[1].strip()
        elif (match := mem_re.match(line)):
            addr, value = map(int, match.groups())
            meme[addr] = apply_mask_p1(mask_str, value)
    print("Init sum:", sum(meme.values()))

    # Part 2 - what a mess
    meme = {}
    for line in lines:
        if line.startswith("mask"):
            mask_str = line.split("=")[1].strip()
            ow_mask = int(mask_str.replace("X", "0"), 2)
            floats = [i for i in range(int_len) if mask_str[::-1][i] == "X"]
        elif (match := mem_re.match(line)):
            addr, value = map(int, match.groups())
            for masked_addr in apply_mask_p2(ow_mask, floats, addr):
                meme[masked_addr] = value
    print("Init sum p2:", sum(meme.values()))


def apply_mask_p1(mask, value):
    value &= int(mask.replace("X", "1"), 2)
    return value | int(mask.replace("X", "0"), 2)


def apply_mask_p2(ow_mask, floats, value):
    value |= ow_mask
    for bitbuffer in range(2 ** len(floats)):
        new_value = value
        for i, f in enumerate(floats):
            bitbuffer_pos = 1 << i
            bit_pos = 1 << f
            if bitbuffer & bitbuffer_pos != 0:
                new_value |= bit_pos
            else:
                new_value &= ~bit_pos
        yield new_value


if __name__ == "__main__":
    main()

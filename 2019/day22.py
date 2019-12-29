"""
Disclaimer: I could not solve part 2 on my own and had to look at some tips
abour modular arithmetic. Gotta gid gud at discrete maths... What I've
understood to get it to work in just a few milliseconds is commented below.

Dumb part 1 is somewhere in Git history.
"""


def main():
    with open("day22.txt") as input_file:
        lines = [l.rstrip() for l in input_file.readlines()]

    # Part 1
    deck_len = 10007
    o, i = shuffle(deck_len, lines)
    print(o, i)
    for n in range(deck_len):
        if (o + i * n) % deck_len == 2019:
            break
    print(f"Position of card 2019: {n}.")

    # Part 2
    deck_len = 119315717514047
    num_shuf = 101741582076661
    o, i = shuffle(deck_len, lines)
    # Each shuffle makes increment a multiple of its previous value % deck_len,
    # and new offset is the old offset incremented by this value.
    # 
    # Using the offset and increment of the first shuffle (O1, I1), we can write
    # a function for n shuffles as they will use those same values:
    # On = On-1 + (In * O1)  % deck_len
    # In = In-1 * I1         % deck_len
    # 
    # We observe that the increment for n shuffles is I1^n-1 % deck_len.
    # 
    # We observe that the offset is dependent of each previous increment value:
    #     O0 = 0
    #     O1 = k
    #     O2 = k + I2*k  (or: O1 + I2*O1)
    #     O3 = k + I2*O1 + I3*O2  (or: O2 + I3*O2)
    #     and this can be factorised as:
    #     On = k * (1 + I1 + I2 + ... + In-1)  % deck_len
    # This expression corresponds to a geometric series, which has a formula to
    # calculate its n-point value, here for our offset function:
    #     On = O1 (1 - I1^n) (1 - I1)^n
    inc_n = pow(i, num_shuf, deck_len)
    ofs_n_op1 = 1 - pow(i, num_shuf, deck_len)
    ofs_n_op2 = pow(1 - i, deck_len - 2, deck_len)
    ofs_n = (o * ofs_n_op1 * ofs_n_op2) % deck_len
    print(f"Card at pos 2020: {(ofs_n + inc_n * 2020) % deck_len}")

def shuffle(deck_len, raw_commands):
    commands = parse_commands(raw_commands)
    offset, inc = 0, 1
    for c, a in commands:
        if c == "dins":
            inc = -inc
            offset += inc
        elif c == "cut":
            offset += inc * a
        elif c == "dwi":
            inc *= pow(a, deck_len - 2, deck_len)  # Fermat's lil theorem.
        offset %= deck_len
        inc %= deck_len
    return offset, inc

def parse_commands(raw_commands):
    commands = []
    for rc in raw_commands:
        if rc.endswith("k"):
            commands.append(("dins", 0))
            continue
        arg = int(rc[rc.rfind(" "):])
        if rc[0] == "d":
            commands.append(("dwi", arg))
        elif rc[0] == "c":
            commands.append(("cut", arg))
    return commands


if __name__ == "__main__":
    main()

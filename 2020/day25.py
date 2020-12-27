import sys

def main():
    lines = [line.rstrip() for line in sys.stdin]
    cpk, dpk = int(lines[0]), int(lines[1])

    dls = crack(dpk, 7)  # cracking door's key is much quicker
    k = gen_key(cpk, dls)
    print(k)
        
def step(v, sn):
    return (v * sn) % 20201227

def crack(pk, sn):
    i = 0
    v = 1
    while v != pk:
        v = step(v, sn)
        i += 1
    return i

def gen_key(sn, ls):
    v = 1
    for _ in range(ls):
        v = step(v, sn)
    return v

if __name__ == "__main__":
    main()

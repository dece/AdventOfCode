from functools import reduce
from operator import mul

with open("input16.txt") as f:
    line = f.read().rstrip()
fdata = ""
for i in range(len(line) // 2):
    fdata += f"{int(line[i*2:i*2+2], 16):08b}"
version_sum = 0


def parse_packets(data, maxp=None):
    global version_sum
    c = 0
    p = 0
    values = []
    while (maxp is None or p < maxp) and c < len(data) - 8:
        version = int(data[c:c+3], 2)
        version_sum += version
        tid = int(data[c+3:c+6], 2)
        c += 6
        if tid == 4:
            bits = ""
            while True:
                stop_reading = data[c] == "0"
                bits += data[c+1:c+5]
                c += 5
                if stop_reading:
                    break
            values.append(int(bits, 2))
        else:
            if data[c] == "0":
                num_bits = int(data[c+1:c+16], 2)
                c += 16
                nc, nv = parse_packets(data[c:c+num_bits])
            else:
                num_subs = int(data[c+1:c+12], 2)
                c += 12
                nc, nv = parse_packets(data[c:], maxp=num_subs)
            c += nc
            if tid == 0:
                values.append(sum(nv))
            elif tid == 1:
                values.append(reduce(mul, nv, 1))
            elif tid == 2:
                values.append(min(nv))
            elif tid == 3:
                values.append(max(nv))
            elif tid == 5:
                values.append(1 if nv[0] > nv[1] else 0)
            elif tid == 6:
                values.append(1 if nv[0] < nv[1] else 0)
            elif tid == 7:
                values.append(1 if nv[0] == nv[1] else 0)
        p += 1
    return c, values


_, values = parse_packets(fdata)
print(version_sum)
print(values[0])

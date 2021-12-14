from collections import defaultdict
from math import ceil

with open("input14.txt") as f:
    lines = [line.rstrip() for line in f]
template = lines[0]
rules = {k: v for k, v in map(lambda s: s.split(" -> "), lines[2:])}
pairs = defaultdict(int)
for i in range(len(template) - 1):
    pairs[template[i:i+2]] += 1
# N  B  B  B  C  N  C  C  N  B  B  N  B  N  B  B  C  H  B  H  H  B  C  H  B
#  NB BB BB BC CN NC CC CN NB BB BN NB BN NB BB BC CH HB BH HH HB BC CH HB
# N=5, B=11, C=5, H=4, but in pairs N=9, B=21, C=10, H=8
# so if odd: n+1 / 2 elif even: n / 2, which is ceil(n / 2) for both
for step in range(40):
    for pair, n in list(pairs.items()):
        if pairs[pair] == 0:
            continue
        mid = rules[pair]
        new_pair1, new_pair2 = pair[0] + mid, mid + pair[1]
        pairs[pair] -= n
        pairs[new_pair1] += n
        pairs[new_pair2] += n
    if step in (9, 39):
        pcount = defaultdict(int)
        for pair, n in pairs.items():
            for p in pair:
                pcount[p] += n
        tcount = {p: ceil(n / 2) for p, n in pcount.items()}
        most_common = max(tcount, key=lambda p: tcount[p])
        least_common = min(tcount, key=lambda p: tcount[p])
        print(tcount[most_common] - tcount[least_common])

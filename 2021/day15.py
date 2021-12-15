from collections import defaultdict
from math import inf

with open("input15.txt") as f:
    lines = [line.rstrip() for line in f]
plan = [list(map(int, line)) for line in lines]
dim = len(plan)
ndim = dim * 5


# wanted to try something other than the yearly dijkstra, so overkill and
# incomplete bellman-ford, precedents skipped for laughable gains.
def solve(dimension, risk_f):
    dists = defaultdict(lambda: inf)
    dists[(0, 0)] = 0
    changed = True
    while changed:
        changed = False
        for x in range(dimension):
            for y in range(dimension):
                p = (x, y)
                dist = dists[p]
                near = []
                if x > 0:
                    near.append((x - 1, y))
                if x < dimension - 1:
                    near.append((x + 1, y))
                if y > 0:
                    near.append((x, y - 1))
                if y < dimension - 1:
                    near.append((x, y + 1))
                for n in near:
                    nx, ny = n
                    risk = risk_f(nx, ny)
                    if dist + risk < dists[n]:
                        changed = True
                        dists[n] = dist + risk
    return dists


def risk_f1(nx, ny):
    return plan[nx][ny]


def risk_f2(nx, ny):
    risk = (plan[nx % dim][ny % dim] + nx // dim + ny // dim)
    while risk >= 10:
        risk -= 9
    return risk


print(solve(dim, risk_f1)[(dim - 1, dim - 1)])
print(solve(ndim, risk_f2)[(ndim - 1, ndim - 1)])

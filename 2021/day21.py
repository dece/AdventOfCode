from functools import cache

with open("input21.txt") as f:
    lines = [line.rstrip() for line in f]
ipos = (int(lines[0].rsplit()[-1]), int(lines[1].rsplit()[-1]))

pos = list(ipos)
scores = [0, 0]
num_rolls = 0
turn = 0
while scores[0] < 1000 and scores[1] < 1000:
    roll = sum(range(num_rolls + 1, num_rolls + 4))
    num_rolls += 3
    pos[turn] = pos[turn] + roll
    pos[turn] = pos[turn] - ((pos[turn] - 1) // 10) * 10
    scores[turn] += pos[turn]
    turn = (turn + 1) % 2
print(min(scores) * num_rolls)

rolls_prob = [
    a + b + c for a in range(1, 4) for b in range(1, 4) for c in range(1, 4)
]


@cache
def play(pos, scores, turn):
    if scores[0] >= 21:
        return 1, 0
    if scores[1] >= 21:
        return 0, 1

    w1, w2 = 0, 0
    nturn = (turn + 1) % 2
    for r in rolls_prob:
        p = pos[turn] + r
        p = p - ((p - 1) // 10) * 10
        if turn == 0:
            npos = p, pos[1]
            nscores = scores[0] + p, scores[1]
        else:
            npos = pos[0], p
            nscores = scores[0], scores[1] + p
        res1, res2 = play(npos, nscores, nturn)
        w1, w2 = w1 + res1, w2 + res2
    return w1, w2


print(max(play(ipos, (0, 0), 0)))

with open("day10.txt", "rt") as f:
    lines = [line.rstrip() for line in f]

CHARMAP = {"]": "[", ")": "(", "}": "{", ">": "<"}
SCOREMAP = {")": 3, "]": 57, "}": 1197, ">": 25137}
SCOREMAP2 = {"(": 1, "[": 2, "{": 3, "<": 4}

error_score = 0
comp_scores = []
for line in lines:
    corrupted = None
    state = []
    for char in line:
        if char in CHARMAP:
            if state and state[-1] == CHARMAP[char]:
                state.pop()
            else:
                corrupted = char
                break
        else:
            state.append(char)
    if corrupted:
        error_score += SCOREMAP[corrupted]
    else:
        cs = 0
        for char in reversed(state):
            cs = cs * 5 + SCOREMAP2[char]
        comp_scores.append(cs)
print(error_score)
print(list(sorted(comp_scores))[len(comp_scores) // 2])

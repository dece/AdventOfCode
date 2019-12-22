import sys

changes = [int(line.rstrip()) for line in sys.stdin.readlines()]

# Part 1
print("Simple sum:", sum(changes))

# Part 2
freq = 0
history = {0: True}
found = False
while not found:
    for c in changes:
        freq += c
        if freq in history:
            found = True
            break
        history[freq] = True
print("First repeated:", freq)

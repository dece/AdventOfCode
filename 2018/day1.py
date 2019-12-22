import sys

print(sum(int(line.rstrip()) for line in sys.stdin.readlines()))

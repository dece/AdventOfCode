import string

with open("input5.txt") as f:
    line = f.read().rstrip()


def react(line):
    while True:
        previous_length = len(line)
        for letter in string.ascii_lowercase:
            bi1 = letter + chr(ord(letter) ^ 0x20)
            bi2 = bi1[::-1]
            line = line.replace(bi1, "")
            line = line.replace(bi2, "")
        if len(line) == previous_length:
            return line


print(len(react(line)))
print(min(
    len(react(line.replace(letter, "").replace(chr(ord(letter) ^ 0x20), "")))
    for letter in string.ascii_letters
))

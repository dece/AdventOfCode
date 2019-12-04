def main():
    with open("day4.txt", "rt") as input_file:
        first_line = input_file.readlines()[0]
    lower_bound, upper_bound = tuple(first_line.strip().split("-"))
    solve(int(lower_bound), int(upper_bound))

def solve(lower_bound, upper_bound):
    validity_map = map(lambda v: int(is_valid(v)), range(lower_bound, upper_bound))
    print("Num valids:", sum(validity_map))

def is_valid(value):
    return has_adjacents(value) and is_increasing(value)

def has_adjacents(value):
    digits = [get_digit(value, index) for index in range(6)]
    for i in range(6 - 1):
        if digits[i] == digits[i + 1]:
            return True
    return False

def is_increasing(value):
    digits = [get_digit(value, index) for index in range(6)]
    for i in range(6 - 1):
        if digits[i + 1] < digits[i]:
            return False
    return True

def get_digit(value, index):
    return int(str(value)[index])

if __name__ == "__main__":
    main()

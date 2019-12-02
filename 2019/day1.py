def get_fuel(mass):
    return mass // 3 - 2

needed_fuel = 0
with open("day1.txt", "rt") as input_file:
    for line in input_file.readlines():
        mass = int(line.strip())
        fuel = get_fuel(mass)
        needed_fuel += fuel

print(needed_fuel)

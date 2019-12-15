def get_fuel(mass):
    return max(0, mass // 3 - 2)

needed_fuel = 0
with open("day1.txt", "rt") as input_file:
    for line in input_file.readlines():
        mass = int(line.strip())
        fuel = get_fuel(mass)

        # Part 2. Comment from line 11 to 14 included for part 1.
        fuel_for_fuel = fuel
        while fuel_for_fuel > 0:
            fuel_for_fuel = get_fuel(fuel_for_fuel)
            fuel += fuel_for_fuel            
        needed_fuel += fuel

print(needed_fuel)

import itertools
import re


class Moon:

    def __init__(self, coords, velocity):
        self.pos = coords
        self.vel = velocity

    def __str__(self):
        return "{} {}".format(self.pos, self.vel)

    def get_energy(self):
        return self.get_pot_energy() * self.get_kin_energy()

    def get_pot_energy(self):
        return abs(self.pos.x) + abs(self.pos.y) + abs(self.pos.z)

    def get_kin_energy(self):
        return abs(self.vel.x) + abs(self.vel.y) + abs(self.vel.z)


class Vector:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)


def main():
    with open("day12.txt", "rt") as input_file:
        lines = input_file.readlines()
    vector_re = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")
    matches = [vector_re.match(line.rstrip()) for line in lines]
    coords = [Vector(*(int(v) for v in match.groups())) for match in matches]
    moons = [Moon(coord, Vector()) for coord in coords]
    for _ in range(1000):
        do_step(moons)
    print("Total moons energy:", sum(moon.get_energy() for moon in moons))

def do_step(moons):
    apply_gravities(moons)
    apply_velocities(moons)

def apply_gravities(moons):
    for pairs in itertools.combinations(moons, 2):
        apply_gravity(*pairs)

def apply_gravity(a, b):
    for c in ["x", "y", "z"]:
        a_pos_c = getattr(a.pos, c)
        b_pos_c = getattr(b.pos, c)
        a_vel_c = getattr(a.vel, c)
        b_vel_c = getattr(b.vel, c)
        if a_pos_c > b_pos_c:
            setattr(a.vel, c, a_vel_c - 1)
            setattr(b.vel, c, b_vel_c + 1)
        elif a_pos_c < b_pos_c:
            setattr(a.vel, c, a_vel_c + 1)
            setattr(b.vel, c, b_vel_c - 1)

def apply_velocities(moons):
    for moon in moons:
        moon.pos += moon.vel


if __name__ == "__main__":
    main()

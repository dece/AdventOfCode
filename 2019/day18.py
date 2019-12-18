from grid import Grid


def main():
    with open("day18.txt", "rt") as input_file:
        lines = input_file.readlines()
    
    lab = Lab(lines)
    lab.dumb_print()


class Lab(Grid):

    TILE_PATH = "."
    TILE_WALL = "#"
    TILE_START = "@"


if __name__ == "__main__":
    main()

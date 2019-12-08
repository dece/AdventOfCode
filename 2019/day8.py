WIDTH = 25
HEIGHT = 6
NUM_PIXELS = WIDTH * HEIGHT


def main():
    with open("day8.txt", "rt") as input_file:
        data = input_file.readlines()[0].rstrip()

    num_layers = len(data) // NUM_PIXELS
    layers = [data[i * NUM_PIXELS : (i+1) * NUM_PIXELS] for i in range(num_layers)]

    # Part 1
    least_zeros_layer = min(layers, key=lambda layer: sum(d == "0" for d in layer))
    num_ones = sum(d == "1" for d in least_zeros_layer)
    num_twos = sum(d == "2" for d in least_zeros_layer)
    print("Result:", num_ones * num_twos)


if __name__ == "__main__":
    main()

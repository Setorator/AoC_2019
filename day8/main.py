import numpy as np
from PIL import Image


def main1():
    f = open("input.txt")
    img = f.readline()
    f.close()

    width = 25
    height = 6
    num_layers = int(len(img) / height / width)

    layers = np.zeros((num_layers, height, width), dtype=int)

    for l in range(num_layers):
        for y in range(height):
            for x in range(width):
                layers[l][y][x] = img[x + y*width + l*(width*height)]

    best_layer = None
    best_count = 25*25  # Arbitrary large number
    for layer in layers:
        zeroes = np.count_nonzero(layer == 0)
        if zeroes < best_count:
            best_count = zeroes
            best_layer = layer

    ones = np.count_nonzero(best_layer == 1)
    twos = np.count_nonzero(best_layer == 2)

    print("1*2: " + (ones * twos).__str__())


def main2():
    f = open("input.txt")
    img = f.readline()
    f.close()

    width = 25
    height = 6
    num_layers = int(len(img) / height / width)

    visible = np.full((height, width), 2, dtype=int)

    for l in range(num_layers):
        for y in range(height):
            for x in range(width):
                if visible[y][x] == 2:
                    visible[y][x] = img[x + y * width + l * (width * height)]

    # Create a bitmap-image
    img = Image.new('1', (25, 6))
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            pixels[x, y] = (int(visible[y][x]))

    # Zoom image to see the letters
    img.show()


if __name__ == '__main__':
    # Part 1
    # main1()

    # Part 2
    main2()

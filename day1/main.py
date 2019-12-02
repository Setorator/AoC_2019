import math


def calc(val):
    res = math.floor(val / 3)
    return res - 2


def calc_rec(val):
    fuel = calc(val)
    if fuel <= 0:
        return 0
    else:
        return fuel + calc_rec(fuel)


def main(func):
    res = 0
    with open("fuel_input.txt") as f:
        for line in f.readlines():
            res += func(int(line))

    print("Final fuel needed: " + res.__str__())


if __name__ == "__main__":
    # Part 1
    # main(calc)

    # Part 2
    main(calc_rec)

import numpy as np

def main1():
    f = open("input.txt")
    wire1_path = list((i for i in f.readline().split(",")))
    wire2_path = list((i for i in f.readline().split(",")))
    f.close()

    orig_x = 6000
    orig_y = 6000

    def extract_lines(path):
        res = np.zeros((12000, 12000), dtype=int)
        last_x = orig_x
        last_y = orig_y

        for line in path:
            steps = 0
            if line[0] == 'U':
                for i in range(last_y, last_y + int(line[1:])):
                    last_y += 1
                    res[last_x][last_y] = 1

            elif line[0] == 'D':
                for i in range(last_y, last_y - int(line[1:]), -1):
                    last_y -= 1
                    res[last_x][last_y] = 1
            elif line[0] == 'R':
                for i in range(last_x, last_x + int(line[1:])):
                    last_x += 1
                    res[last_x][last_y] = 1
            elif line[0] == 'L':
                for i in range(last_x, last_x - int(line[1:]), -1):
                    last_x -= 1
                    res[last_x][last_y] = 1
            else:
                raise ValueError

        return res


    wire1_map = extract_lines(wire1_path)
    wire2_map = extract_lines(wire2_path)

    closest_distance = 999999999999  # just a very large value

    for x in range(12000):
        for y in range(12000):
            if wire1_map[x][y] > 0 and wire2_map[x][y] > 0:
                dist = abs(x - orig_x) + abs(y - orig_y)
                if dist > 0 and dist < closest_distance:
                    closest_distance = dist


    print("Closest distance: " + closest_distance.__str__())


if __name__ == '__main__':
    main()

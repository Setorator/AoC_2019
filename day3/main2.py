import numpy as np


def main():
    f = open("input.txt")
    wire1_input = list((i for i in f.readline().split(",")))
    wire2_input = list((i for i in f.readline().split(",")))
    f.close()

    orig_x = 6000
    orig_y = 6000

    def extract_lines(path):
        res = np.zeros((12000, 12000), dtype=int)
        travelled_path = []
        last_x = orig_x
        last_y = orig_y

        for line in path:
            if line[0] == 'U':
                for i in range(last_y, last_y + int(line[1:])):
                    last_y += 1
                    res[last_x][last_y] = 1
                    travelled_path.append((last_x, last_y))
            elif line[0] == 'D':
                for i in range(last_y, last_y - int(line[1:]), -1):
                    last_y -= 1
                    res[last_x][last_y] = 1
                    travelled_path.append((last_x, last_y))

            elif line[0] == 'R':
                for i in range(last_x, last_x + int(line[1:])):
                    last_x += 1
                    res[last_x][last_y] = 1
                    travelled_path.append((last_x, last_y))

            elif line[0] == 'L':
                for i in range(last_x, last_x - int(line[1:]), -1):
                    last_x -= 1
                    res[last_x][last_y] = 1
                    travelled_path.append((last_x, last_y))

            else:
                raise ValueError

        return res, travelled_path

    wire1_map, wire1_path = extract_lines(wire1_input)
    wire2_map, wire2_path = extract_lines(wire2_input)
    collision_map = []

    closest_distance = 999999999999  # just a very large value

    for x in range(12000):
        for y in range(12000):
            if wire1_map[x][y] > 0 and wire2_map[x][y] > 0:
                collision_map.append((x, y))
                dist = abs(x - orig_x) + abs(y - orig_y)
                if dist > 0 and dist < closest_distance:
                    closest_distance = dist

    print("Closest distance: " + closest_distance.__str__())

    travel_path1 = 0
    travel_path2 = 0
    travel_path_best = 99999999  # arbitrary big value

    for collision in collision_map:
        for step1 in wire1_path:
            travel_path1 += 1
            if step1 == collision:
                for step2 in wire2_path:
                    travel_path2 += 1
                    if step2 == collision:
                        if travel_path1 + travel_path2 < travel_path_best:
                            travel_path_best = travel_path2 + travel_path1

                        travel_path2 = 0
                        break
                travel_path1 = 0
                break

    print("Smallest distance: " + travel_path_best.__str__())


if __name__ == '__main__':
    main()

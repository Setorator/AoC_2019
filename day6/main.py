
def main():
    orbits = {}

    def dist(p, s):
        if p not in orbits:
            return s
        else:
            res = s
            for orbit in orbits[p]:
                res += dist(orbit, s + 1)
            return res

    def dist_to_com(goal, s):
        path_to_com = []
        for i in orbits:
            if goal in orbits[i]:
                path_to_com += [(i, s)] + dist_to_com(i, s + 1)
                break

        return path_to_com

    with open("input.txt") as f:
        for line in f.readlines():
            planet = line.split(")")[0].strip()
            in_orbit = line.split(")")[1].strip()

            if planet in orbits:
                orbits[planet] += [in_orbit]
            else:
                orbits[planet] = [in_orbit]

    root = None
    for outer in orbits:
        is_root = True
        for inner in orbits:
            if outer in orbits[inner]:
                is_root = False
        if is_root:
            root = outer
            break

    print("Total orbital distances: " + dist(root, 0).__str__())

    # Part 2
    your_path_to_com = dist_to_com("YOU", 0)
    santas_path_to_com = dist_to_com("SAN", 0)
    dist_you_santa = 0

    e = False
    for node_y, dist_y in your_path_to_com:
        for node_s, dist_s in santas_path_to_com:
            if node_y == node_s:
                dist_you_santa = dist_y + dist_s
                e = True
                break
        if e:
            break

    print("Distance from you to Santa: " + dist_you_santa.__str__())


if __name__ == '__main__':
    main()

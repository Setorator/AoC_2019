import math


def main():
    aster_map = []

    with open("input.txt") as f:
        lines = f.readlines()
        for y in range(len(lines)):
            for x in range(len(lines[0].strip())):
                if lines[y][x] == "#":
                    aster_map.append((x, y))

    best_loc = (0, 0)
    best_tot = 0
    best_detec = {}

    # Find all asteroids on a different angle from the station, using tan
    for station in aster_map:
        angles = {}
        for aster in aster_map:
            if aster is not station:
                angle = math.atan2(station[1] - aster[1], station[0] - aster[0])
                if angle not in angles:
                    angles[angle] = (aster[0], aster[1])

                # If there is already an asteroid on this angle, but it is
                # further away than this one, replace it
                elif angle in angles:
                    if math.hypot(aster[0], aster[1]) < math.hypot(angles[angle][0], angles[angle][1]):
                        angles[angle] = (aster[0], aster[1])

        if len(angles) > best_tot:
            best_loc = station
            best_tot = len(angles)
            best_detec = angles

    print("Station: {}".format(best_loc))
    print("Num detections: {}".format(best_tot))

    return best_loc, best_tot, best_detec


def main2(num_aster, locs):
    tot_dest = 0
    direction = math.pi/2
    order = []

    switch_ind = 0
    pi_break = True

    while tot_dest < num_aster:
        highest_rad = max(locs)

        # The second quadrant (top left) should be taken last
        if highest_rad < direction and pi_break:
            switch_ind = tot_dest
            pi_break = False

        order.append(locs.pop(highest_rad))

        tot_dest += 1

    # Move the second quadrant last in the order and reverse each part ([::-1])
    # This is needed since the atan2() is calculated using relative coordinates
    # instead of absolute.
    order = order[:switch_ind][::-1] + order[switch_ind:][::-1]

    print("Num 200: {}".format(order[199]))


if __name__ == '__main__':
    new_station, tot_found, locations = main()

    main2(tot_found, locations)

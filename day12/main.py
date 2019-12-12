import numpy as np


def main():

    # Input
    io_pos = np.array([6, 10, 10], dtype=int)
    eur_pos = np.array([-9, 3, 17], dtype=int)
    gan_pos = np.array([9, -4, 14], dtype=int)
    cal_pos = np.array([4, 14, 4], dtype=int)

    init_pos = np.array([io_pos, eur_pos, gan_pos, cal_pos])
    moons_pos = np.array([io_pos, eur_pos, gan_pos, cal_pos])

    io_vel = np.zeros(3, dtype=int)
    eur_vel = np.zeros(3, dtype=int)
    gan_vel = np.zeros(3, dtype=int)
    cal_vel = np.zeros(3, dtype=int)

    # The first repetition will be the initial state, since there is only one previous state that could have led to it.
    init_vel = np.array([io_vel, eur_vel, gan_vel, cal_vel])
    moons_vel = np.array([io_vel, eur_vel, gan_vel, cal_vel])

    steps = 0

    found_moon = [False, False, False]
    step_at = []

    while not all(found_moon):

        # Divide and conquer
        # Find, for each axis, where it has the same state as in the initial state.
        # Then take the least common multiple of the three axis to find the first repetition
        if steps > 0:
            for i in range(3):
                if not found_moon[i] and np.array_equal(moons_pos[:, i], init_pos[:, i]) and np.array_equal(moons_vel[:, i], init_vel[:, i]):
                    found_moon[i] = True
                    step_at.append(steps)

        # Apply Gravity
        for moon1 in range(len(moons_pos)):
            for moon2 in range(moon1 + 1, len(moons_pos)):

                for axis in range(len(moons_pos[moon1])):
                    if moons_pos[moon1][axis] > moons_pos[moon2][axis]:
                        moons_vel[moon1][axis] -= 1
                        moons_vel[moon2][axis] += 1
                    elif moons_pos[moon1][axis] < moons_pos[moon2][axis]:
                        moons_vel[moon1][axis] += 1
                        moons_vel[moon2][axis] -= 1

        # Update positions
        moons_pos += moons_vel

        print("Steps: {}".format(steps))
        steps += 1

    print(step_at.__str__())
    print(np.lcm.reduce(step_at))


if __name__ == '__main__':
    main()

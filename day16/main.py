import numpy as np


def main():
    with open("input.txt") as f:
        line = f.readline()
        trans_orig = np.array([int(i) for i in line] * 10000)
        offset = int(line[:7])

    trans = trans_orig
    p = np.array([0, 1, 0, -1])
    pattern = np.zeros(np.size(trans), dtype=int)
    patterns = []

    for i in range(np.size(trans)):
        print("Step: {}".format(i))
        rep = i + 1

        # Form the pattern array
        j = 0
        pat_i = 0
        while j < np.size(pattern) + 1:

            for k in range(rep):
                # Skip first value
                if not (j == 0 and k == 0):
                    if j + rep < np.size(pattern) + 1:
                        pattern[j-1: j-1 + rep] = [p[pat_i]] * rep
                        j += rep
                        break
                    elif j < np.size(pattern) + 1:
                        pattern[j-1] = p[pat_i]
                        j += 1

                else:
                    if j + rep - 1 < np.size(pattern) + 1:
                        pattern[j: j + rep - 1] = [p[pat_i]] * (rep-1)
                        j += rep
                        break
                    else:
                        pattern.fill(0)
                        break

            pat_i = (pat_i + 1) % 4
        patterns.append(np.copy(pattern))

    for phase in range(100):
        tmp_trans = np.zeros(np.size(trans), dtype=int)
        for i in range(np.size(trans)):
            tmp_trans[i] = int(np.dot(trans, patterns[i]).__str__()[-1])
        trans = tmp_trans

    print("Trans after 100 phases: {}".format(trans.__str__()))
    print("with offset: {}".format(trans[5977341:5977341+8]))


if __name__ == '__main__':
    main()

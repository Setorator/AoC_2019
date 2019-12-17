import numpy as np


def calc_modes(m):
    mode_code = m.__str__()[:-2]
    modes = [0, 0, 0]  # a, b, c
    for i in range(len(mode_code)):
        modes[i] = int(mode_code[-1-i])
    return modes


class IntCode:

    def __init__(self):
        f = open("input.txt")
        self.code = list((int(i) for i in f.readline().split(",")))
        f.close()
        self.program_len = len(self.code)

        self.relative_base = 0
        self.mem = np.zeros(self.program_len*20, dtype=np.int64)
        self.mem[0:self.program_len] = self.code

        self.map = np.zeros((100, 100), dtype=str)
        self.intersections = {}

        self.code_cnt = 0
        self.out = 0
        self.out_ind = [0, 0]
        self.arg_i = 0
        self.num_blocks = 0

    def intersec(self, y_i, x_i):
        if self.map[y_i - 1, x_i] == '#' and self.map[y_i + 1, x_i] == '#':
            if self.map[y_i, x_i - 1] == '#' and self.map[y_i, x_i + 1] == '#':
                return True
        return False

    def run(self, args):

        def addr(arg_i):
            if par_modes[arg_i] == 0:
                return self.mem[self.code_cnt + 1 + arg_i]
            elif par_modes[arg_i] == 1:
                return self.code_cnt + 1 + arg_i
            elif par_modes[arg_i] == 2:
                return self.mem[self.code_cnt + 1 + arg_i] + self.relative_base
            else:
                raise ValueError

        while self.code_cnt < self.program_len:
            op_code = int(self.mem[self.code_cnt].__str__()[-2:])
            par_modes = calc_modes(self.mem[self.code_cnt])

            if op_code == 1:
                self.mem[addr(2)] = self.mem[addr(0)] + self.mem[addr(1)]
                self.code_cnt += 4

            elif op_code == 2:
                self.mem[addr(2)] = self.mem[addr(0)] * self.mem[addr(1)]
                self.code_cnt += 4

            elif op_code == 3:
                self.mem[addr(0)] = ord(args[self.arg_i])
                self.code_cnt += 2
                self.arg_i += 1

            elif op_code == 4:
                self.out = self.mem[addr(0)]
                if self.out != 10:
                    self.map[self.out_ind[0], self.out_ind[1]] = chr(self.out)
                    self.out_ind[1] += 1
                else:
                    print(''.join(map(str, self.map[self.out_ind[0]])))
                    self.out_ind[0] += 1
                    self.out_ind[1] = 0

                self.code_cnt += 2

            elif op_code == 5:
                if self.mem[addr(0)] != 0:
                    self.code_cnt = self.mem[addr(1)]
                else:
                    self.code_cnt += 3

            elif op_code == 6:
                if self.mem[addr(0)] == 0:
                    self.code_cnt = self.mem[addr(1)]
                else:
                    self.code_cnt += 3

            elif op_code == 7:
                if self.mem[addr(0)] < self.mem[addr(1)]:
                    self.mem[addr(2)] = 1
                else:
                    self.mem[addr(2)] = 0
                self.code_cnt += 4

            elif op_code == 8:
                if self.mem[addr(0)] == self.mem[addr(1)]:
                    self.mem[addr(2)] = 1
                else:
                    self.mem[addr(2)] = 0
                self.code_cnt += 4

            elif op_code == 9:
                self.relative_base += self.mem[addr(0)]
                self.code_cnt += 2

            elif op_code == 99:
                print("Total dust collected: {}".format(self.out))
                self.out = None
                break
            else:
                print("Found value " + self.mem[self.code_cnt].__str__() + " at position " + self.code_cnt.__str__())
                raise ModuleNotFoundError

        # Part 1
        for y in range(np.size(self.map, 0)-1):
            for x in range(np.size(self.map, 1)):
                # check if intersection
                if self.map[y, x] == '#' and self.intersec(y, x):
                    self.intersections[(y, x)] = y * x

        res = 0
        for inter in self.intersections:
            res += self.intersections[inter]

        print("Alignment param. sum: {}".format(res))


if __name__ == '__main__':
    comp = IntCode()

    # Part 2
    comp.mem[0] = 2
    args = ""

    # Main movement
    args += "A,A,B,C,B,C,B,C,C,A\n"

    # Function A
    args += "R,8,L,4,R,4,R,10,R,8\n"

    # Function B
    args += "L,12,L,12,R,8,R,8\n"

    # Function C
    args += "R,10,R,4,R,4\n"

    # Video feed
    args += "n\n"

    # Send in all the arguments at once
    comp.run(args)

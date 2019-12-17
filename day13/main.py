import numpy as np


def calc_modes(m):
    mode_code = m.__str__()[:-2]
    modes = [0, 0, 0]  # a, b, c
    for i in range(len(mode_code)):
        modes[i] = int(mode_code[-1-i])
    return modes


class Arcade:

    def __init__(self):
        f = open("input.txt")
        self.code = list((int(i) for i in f.readline().split(",")))
        f.close()
        self.program_len = len(self.code)

        self.relative_base = 0
        self.mem = np.zeros(self.program_len*20, dtype=np.int64)
        self.mem[0:self.program_len] = self.code

        self.map = np.zeros((26, 42), dtype=int)

        self.code_cnt = 0
        self.out = [0, 0, 0]
        self.out_ind = 0
        self.num_blocks = 0

    def run(self):

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
                for row in self.map:
                    print(list(row))
                self.mem[addr(0)] = 0
                self.code_cnt += 2

            elif op_code == 4:
                # First output is the color to paint the panel with,
                # Second is the angle to rotate
                self.out[self.out_ind] = self.mem[addr(0)]
                self.code_cnt += 2
                if self.out_ind == 2:
                    self.out_ind = 0
                    if self.out[0] == -1 and self.out[1] == 0:
                        print("Score: {}".format(self.out[2]))

                    else:
                        if self.out[2] == 2:
                            self.num_blocks += 1
                        self.map[self.out[1]][self.out[0]] = self.out[2]

                else:
                    self.out_ind += 1

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
                self.out = None
                break
            else:
                print("Found value " + self.mem[self.code_cnt].__str__() + " at position " + self.code_cnt.__str__())
                raise ModuleNotFoundError

        print("Num blocks: {}".format(self.num_blocks))


if __name__ == '__main__':
    a = Arcade()
    a.run()

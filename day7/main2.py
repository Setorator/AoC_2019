import itertools


def add(x, y):
    return x + y


def mult(x, y):
    return x * y


def calc_modes(m):
    mode_code = m.__str__()[:-2]
    modes = [0, 0, 0]  # a, b, c
    for i in range(len(mode_code)):
        modes[i] = int(mode_code[-1 - i])
    return modes


class Amp:

    def __init__(self):
        f = open("input_day7.txt")
        self.code = list((int(i) for i in f.readline().split(",")))
        f.close()
        self.code_cnt = 0
        self.out = 0
        self.args_ind = 0

    def run(self, args):
        program_len = len(self.code)

        def value(par_i, par):
            if par_modes[par_i] == 0:
                return self.code[par]
            elif par_modes[par_i] == 1:
                return par
            else:
                raise ValueError

        while self.code_cnt < program_len:
            op_code = int(self.code[self.code_cnt].__str__()[-2:])
            par_modes = calc_modes(self.code[self.code_cnt])

            if op_code == 1:
                add_par_1 = value(0, self.code[self.code_cnt+1])
                add_par_2 = value(1, self.code[self.code_cnt+2])
                self.code[self.code[self.code_cnt + 3]] = add(add_par_1, add_par_2)
                self.code_cnt += 4

            elif op_code == 2:
                mult_par_1 = value(0, self.code[self.code_cnt + 1])
                mult_par_2 = value(1, self.code[self.code_cnt + 2])
                self.code[self.code[self.code_cnt + 3]] = mult(mult_par_1, mult_par_2)
                self.code_cnt += 4

            elif op_code == 3:
                self.code[self.code[self.code_cnt + 1]] = args[self.args_ind]
                self.code_cnt += 2
                if self.args_ind < 1:
                    self.args_ind += 1

            elif op_code == 4:
                self.out = value(0, self.code[self.code_cnt + 1])
                self.code_cnt += 2
                break

            elif op_code == 5:
                if value(0, self.code[self.code_cnt + 1]) != 0:
                    self.code_cnt = value(1, self.code[self.code_cnt + 2])
                else:
                    self.code_cnt += 3

            elif op_code == 6:
                if value(0, self.code[self.code_cnt + 1]) == 0:
                    self.code_cnt = value(1, self.code[self.code_cnt + 2])
                else:
                    self.code_cnt += 3

            elif op_code == 7:
                if value(0, self.code[self.code_cnt + 1]) < value(1, self.code[self.code_cnt + 2]):
                    self.code[self.code[self.code_cnt + 3]] = 1
                else:
                    self.code[self.code[self.code_cnt + 3]] = 0
                self.code_cnt += 4

            elif op_code == 8:
                if value(0, self.code[self.code_cnt + 1]) == value(1, self.code[self.code_cnt + 2]):
                    self.code[self.code[self.code_cnt + 3]] = 1
                else:
                    self.code[self.code[self.code_cnt + 3]] = 0
                self.code_cnt += 4

            elif op_code == 99:
                print("returns None")
                self.out = None
                break
            else:
                print("Found value " + self.code[self.code_cnt].__str__() + " at position " + self.code_cnt.__str__())
                raise ModuleNotFoundError


def main():

    perms = list(itertools.permutations([5, 6, 7, 8, 9]))
    best = 0

    for perm in perms:
        # init
        amp_a = Amp()
        amp_b = Amp()
        amp_c = Amp()
        amp_d = Amp()
        amp_e = Amp()

        amp_a.run([perm[0], 0])
        amp_b.run([perm[1], amp_a.out])
        amp_c.run([perm[2], amp_b.out])
        amp_d.run([perm[3], amp_c.out])
        amp_e.run([perm[4], amp_d.out])

        while True:
            amp_a.run([None, amp_e.out])

            if amp_a.out is None:
                if amp_e.out > best:
                    best = amp_e.out
                    print("New best: " + best.__str__())
                break

            amp_b.run([None, amp_a.out])
            amp_c.run([None, amp_b.out])
            amp_d.run([None, amp_c.out])
            amp_e.run([None, amp_d.out])

    print(best.__str__())


if __name__ == '__main__':
    main()

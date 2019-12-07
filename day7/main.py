import itertools

def add(x, y):
    return x + y


def mult(x, y):
    return x * y


def calc_modes(m):
    mode_code = m.__str__()[:-2]
    modes = [0, 0, 0]  # a, b, c
    for i in range(len(mode_code)):
        modes[i] = int(mode_code[-1-i])
    return modes


def run(code, args):
    """
    Modded version of the Intcode computer that reads from an input list and returns output instead
    of prompting user.
    :param code: The program to be run
    :param args: The argument list
    :return: The output of the amplifier
    """
    program_len = len(code)
    input_ind = 0
    res = None

    def value(par_i, par):
        if par_modes[par_i] == 0:
            return code[par]
        elif par_modes[par_i] == 1:
            return par
        else:
            raise ValueError

    i = 0
    while i < program_len:
        op_code = int(code[i].__str__()[-2:])
        par_modes = calc_modes(code[i])

        if op_code == 1:
            add_par_1 = value(0, code[i+1])
            add_par_2 = value(1, code[i+2])
            code[code[i + 3]] = add(add_par_1, add_par_2)
            i += 4

        elif op_code == 2:
            mult_par_1 = value(0, code[i + 1])
            mult_par_2 = value(1, code[i + 2])
            code[code[i + 3]] = mult(mult_par_1, mult_par_2)
            i += 4

        elif op_code == 3:
            code[code[i + 1]] = args[input_ind]
            input_ind += 1
            i += 2

        elif op_code == 4:
            res = value(0, code[i + 1])
            i += 2

        elif op_code == 5:
            if value(0, code[i + 1]) != 0:
                i = value(1, code[i + 2])
            else:
                i += 3

        elif op_code == 6:
            if value(0, code[i + 1]) == 0:
                i = value(1, code[i + 2])
            else:
                i += 3

        elif op_code == 7:
            if value(0, code[i + 1]) < value(1, code[i + 2]):
                code[code[i + 3]] = 1
            else:
                code[code[i + 3]] = 0
            i += 4

        elif op_code == 8:
            if value(0, code[i + 1]) == value(1, code[i + 2]):
                code[code[i + 3]] = 1
            else:
                code[code[i + 3]] = 0
            i += 4

        elif op_code == 99:
            return res
        else:
            print("Found value " + code[i].__str__() + " at position " + i.__str__())
            raise ModuleNotFoundError


def main():
    f = open("input_day7.txt")
    code = list((int(i) for i in f.readline().split(",")))
    f.close()

    best = 0
    perms = list(itertools.permutations([0,1,2,3,4]))

    for perm in perms:
        out_a = run(code, [perm[0], 0])
        out_b = run(code, [perm[1], out_a])
        out_c = run(code, [perm[2], out_b])
        out_d = run(code, [perm[3], out_c])
        out_e = run(code, [perm[4], out_d])

        if out_e > best:
            best = out_e

    print(best.__str__())


if __name__ == '__main__':
    main()


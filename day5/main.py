import copy


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


def main():
    f = open("input.txt")
    code = list((int(i) for i in f.readline().split(",")))
    f.close()
    program_len = len(code)

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
            code[code[i + 1]] = int(input())
            i += 2

        elif op_code == 4:
            print(value(0, code[i + 1]))
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
            break
        else:
            print("Found value " + code[i].__str__() + " at position " + i.__str__())
            raise ModuleNotFoundError


if __name__ == '__main__':
    main()


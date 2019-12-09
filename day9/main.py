import numpy as np


def calc_modes(m):
    mode_code = m.__str__()[:-2]
    modes = [0, 0, 0]  # a, b, c
    for i in range(len(mode_code)):
        modes[i] = int(mode_code[-1-i])
    return modes


def run(code):
    program_len = len(code)
    relative_base = 0
    mem = np.zeros(program_len*20, dtype=np.int64)
    mem[0:program_len] = code

    i = 0

    def addr(arg_i):
        if par_modes[arg_i] == 0:
            return mem[i + 1 + arg_i]
        elif par_modes[arg_i] == 1:
            return i + 1 + arg_i
        elif par_modes[arg_i] == 2:
            return mem[i + 1 + arg_i] + relative_base
        else:
            raise ValueError

    while i < program_len:
        op_code = int(mem[i].__str__()[-2:])
        par_modes = calc_modes(mem[i])

        if op_code == 1:
            mem[addr(2)] = mem[addr(0)] + mem[addr(1)]
            i += 4

        elif op_code == 2:
            mem[addr(2)] = mem[addr(0)] * mem[addr(1)]
            i += 4

        elif op_code == 3:
            mem[addr(0)] = int(input())
            i += 2

        elif op_code == 4:
            print(mem[addr(0)])
            i += 2

        elif op_code == 5:
            if mem[addr(0)] != 0:
                i = mem[addr(1)]
            else:
                i += 3

        elif op_code == 6:
            if mem[addr(0)] == 0:
                i = mem[addr(1)]
            else:
                i += 3

        elif op_code == 7:
            if mem[addr(0)] < mem[addr(1)]:
                mem[addr(2)] = 1
            else:
                mem[addr(2)] = 0
            i += 4

        elif op_code == 8:
            if mem[addr(0,)] == mem[addr(1)]:
                mem[addr(2,)] = 1
            else:
                mem[addr(2,)] = 0
            i += 4

        elif op_code == 9:
            relative_base += mem[addr(0)]
            i += 2

        elif op_code == 99:
            break
        else:
            print("Found value " + mem[i].__str__() + " at position " + i.__str__())
            raise ModuleNotFoundError


def main():
    f = open("input.txt")
    code = list((int(i) for i in f.readline().split(",")))
    f.close()
    run(code)


if __name__ == '__main__':
    main()


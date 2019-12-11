import numpy as np
from PIL import Image


def calc_modes(m):
    mode_code = m.__str__()[:-2]
    modes = [0, 0, 0]  # a, b, c
    for i in range(len(mode_code)):
        modes[i] = int(mode_code[-1-i])
    return modes


class Brain:

    def __init__(self):
        f = open("input.txt")
        self.code = list((int(i) for i in f.readline().split(",")))
        f.close()
        self.program_len = len(self.code)

        self.relative_base = 0
        self.mem = np.zeros(self.program_len*20, dtype=np.int64)
        self.mem[0:self.program_len] = self.code

        self.code_cnt = 0
        self.out = [0, 0]
        self.out_ind = 0

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
                self.mem[addr(0)] = args
                self.code_cnt += 2

            elif op_code == 4:
                # First output is the color to paint the panel with,
                # Second is the angle to rotate
                self.out[self.out_ind] = self.mem[addr(0)]
                self.code_cnt += 2
                if self.out_ind == 1:
                    self.out_ind = 0
                    break
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


def main(arg):
    rob_map = np.zeros((200, 200), dtype=int)

    # (0,1,2,3) = (<,^,>,V)
    rob_dir = 1
    rob_headings = ((-1, 0), (0, 1), (1, 0), (0, -1))
    rob_pos = (int(np.size(rob_map, 1)/2), int(np.size(rob_map, 0)/2))
    rob_visited = []

    rob_map[rob_pos] = arg
    brain = Brain()
    brain.run(rob_map[rob_pos])

    while brain.out is not None:

        # Paint panel
        rob_map[rob_pos] = brain.out[0]

        # Rotate robot
        if brain.out[1] == 0:
            if rob_dir == 0:
                rob_dir = 3
            else:
                rob_dir -= 1
        elif brain.out[1] == 1:
            if rob_dir == 3:
                rob_dir = 0
            else:
                rob_dir += 1

        # move robot
        if rob_pos not in rob_visited:
            rob_visited.append(rob_pos)

        new_x = rob_pos[0] + rob_headings[rob_dir][0]
        new_y = rob_pos[1] + rob_headings[rob_dir][1]
        rob_pos = (new_x, new_y)

        # Paint
        brain.run(rob_map[rob_pos])

    print("Painted: {}".format(len(rob_visited)))

    # Create a bitmap-image
    img = Image.new('1', (np.size(rob_map, 0), np.size(rob_map, 1)))
    pixels = img.load()
    for y in range(np.size(rob_map, 0)):
        for x in range(np.size(rob_map, 1)):
            pixels[x, y] = (int(rob_map[y][x]))

    # Zoom image to see the letters
    img.show()


if __name__ == '__main__':
    # input 0 for part 1 and 1 for part 2
    main(1)

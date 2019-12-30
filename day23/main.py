import numpy as np
import queue
from copy import deepcopy


def calc_modes(m):
    mode_code = m.__str__()[:-2]
    modes = [0, 0, 0]  # a, b, c
    for i in range(len(mode_code)):
        modes[i] = int(mode_code[-1-i])
    return modes


class Computer:

    def __init__(self, my_id):
        f = open("input.txt")
        self.code = list((int(i) for i in f.readline().split(",")))
        f.close()
        self.program_len = len(self.code)

        self.relative_base = 0
        self.mem = np.zeros(self.program_len*20, dtype=np.int64)
        self.mem[0:self.program_len] = self.code

        self.code_cnt = 0
        self.args = None
        self.arg_ind = -1
        self.out = [None, None, None]
        self.out_ind = 0

        self.id = my_id

        self.idle_cnt = 0
        idle_stat[self.id] = False

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
                if self.arg_ind == -1:
                    self.mem[addr(0)] = self.id
                    self.arg_ind = 0

                elif mess_queue[self.id].empty() and self.arg_ind == 0:
                    self.mem[addr(0)] = -1
                    self.idle_cnt += 1

                else:
                    self.idle_cnt = 0
                    idle_stat[self.id] = False
                    if self.arg_ind == 0 and self.args is None:
                        self.args = mess_queue[self.id].get()
                        print("Thread {} got message {}".format(self.id, self.args))

                    self.mem[addr(0)] = self.args[self.arg_ind]
                    self.arg_ind += 1

                    if self.arg_ind == 2:
                        self.args = None
                        self.arg_ind = 0

                # If there has been no new messages for 3 iterations, set status to idle
                if self.idle_cnt > 2:
                    idle_stat[self.id] = True

                self.code_cnt += 2
                break

            elif op_code == 4:
                self.out[self.out_ind] = self.mem[addr(0)]
                self.out_ind += 1

                if self.out_ind == 3:
                    mess_queue[self.out[0]].put((self.out[1], self.out[2]))
                    print("Thread {} sent {} to thread {}".format(self.id, (self.out[1], self.out[2]), self.out[0]))
                    self.out_ind = 0

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
                self.out = None
                break
            else:
                print("Found value " + self.mem[self.code_cnt].__str__() + " at position " + self.code_cnt.__str__())
                raise ModuleNotFoundError


if __name__ == '__main__':

    comp_list = []
    mess_queue = {}
    idle_stat = [False] * 50

    # Init threads and message queues
    for c in range(50):
        mess_queue[c] = queue.Queue()
        tmp = Computer(c)
        comp_list.append(tmp)

    mess_queue[255] = queue.Queue()
    finished = False
    last_sent = None
    last_received = None

    while not finished:

        # Perform one iteration of computers
        for c in comp_list:
            c.run()

        # Check for messages to NAT
        if not mess_queue[255].empty():
            last_received = mess_queue[255].get()

        # If all computers are set to idle (value True)
        elif all(idle_stat) and last_received is not None:
            if last_sent is not None and last_sent[1] == last_received[1]:
                print("FOUND MATCH:{}!".format(last_received[1]))
                finished = True
                break

            idle_stat = [False] * 50

            mess_queue[0].put(last_received)
            last_sent = deepcopy(last_received)
            # First print of this line is answer for part 1
            print("Sent package {} to address 0".format(last_received))

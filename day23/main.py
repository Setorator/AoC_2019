import numpy as np
import threading
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

    def __call__(self):

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
                    self.idle_cnt = 0
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

                if self.idle_cnt > 100:
                    idle_stat[self.id] = True

                self.code_cnt += 2

            elif op_code == 4:
                self.out[self.out_ind] = self.mem[addr(0)]
                self.out_ind += 1

                if self.out_ind == 3:

                    # Part 1
                    if self.out[0] == 255:
                        print("For 255, X is {} and Y is {}".format(self.out[1], self.out[2]))

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
                print("Last op code was {}".format(self.last_op))
                raise ModuleNotFoundError


# Part 2
def NAT():
    last_sent = None
    last_package = None
    global idle_stat
    done = False

    while not done:
        if not mess_queue[255].empty():
            last_package = mess_queue[255].get()
            print("255 got package {}".format(last_package))

        # If all computers are set to idle (value True)
        elif all(idle_stat) and last_package is not None and all(mess_queue[s].empty() for s in mess_queue):
            if last_sent is not None and last_sent[1] == last_package[1]:
                print("FOUND MATCH: {}-{}!".format(last_sent[1], last_package[1]))
                done = True
                break

            mess_queue[0].put(last_package)

            # Change stat of all computers to "non-idle"
            idle_stat = [False] * 50

            print("255 Sent {} to address 0".format(last_package))

            last_sent = deepcopy(last_package)



if __name__ == '__main__':

    comp_list = []
    mess_queue = {}
    mess_queue[255] = queue.Queue()

    # Part 2
    idle_stat = [False] * 50
    nat_thread = threading.Thread(target=NAT)
    nat_thread.start()

    # Init threads and message queues
    for i in range(50):
        mess_queue[i] = queue.Queue()
        tmp = threading.Thread(target=Computer(i))
        comp_list.append(tmp)

    # Start threads
    for i in range(50):
        comp_list[i].start()

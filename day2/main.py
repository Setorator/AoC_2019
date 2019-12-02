import copy

def add(x, y):
    return x + y


def mult(x, y):
    return x * y


def main1():
    f = open("input.txt")
    code = list((int(i) for i in f.readline().split(",")))
    f.close()

    for i in range(0, len(code), 4):
        if code[i] == 1:
            code[code[i + 3]] = add(code[code[i + 1]], code[code[i + 2]])
        elif code[i] == 2:
            code[code[i + 3]] = mult(code[code[i + 1]], code[code[i + 2]])
        elif code[i] == 99:
            break
        else:
            print("Found value " + code[i].__str__() + " at position " + i.__str__())
            raise ModuleNotFoundError

    print(code)


def main2():
    f = open("input.txt")
    orig_code = list((int(i) for i in f.readline().split(",")))
    f.close()

    for noun in range(100):
        for verb in range(100):
            code = copy.deepcopy(orig_code)
            code[1] = noun
            code[2] = verb
            for i in range(0, len(code), 4):
                if code[i] == 1:
                    code[code[i+3]] = add(code[code[i+1]], code[code[i+2]])
                elif code[i] == 2:
                    code[code[i+3]] = mult(code[code[i+1]], code[code[i+2]])
                elif code[i] == 99:
                    break
                else:
                    print("Found value " + code[i].__str__() + " at position " + i.__str__())
                    raise ModuleNotFoundError

            if code[0] == 19690720:
                print("Noun: " + noun.__str__())
                print("Verb: " + verb.__str__())
                break


if __name__ == '__main__':
    # Part 1
    # main1()

    # Part 2
    main2()

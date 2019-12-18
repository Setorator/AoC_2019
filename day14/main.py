

def strip_int(val):
    # Returns the int part and the material part
    for i in range(len(val)):
        try:
            int(val[i])
        except ValueError:
            return int(val[:i]), val[i+1:]


if __name__ == '__main__':
    reactions = {}
    available_chems = {}
    used_ore = 0


    def trigger_reac(reac):
        global used_ore
        for chem in reactions[reac]["chems"]:
            i, c = strip_int(chem)

            if c == "ORE":
                used_ore += i
                break

            # Gather lower material if needed
            while available_chems[c] < i:
                trigger_reac(c)

            # When there is enough sub-material, perform reaction
            available_chems[c] -= i
        # Append amount to available-dict
        available_chems[reac] += reactions[reac]["amount"]


    def trigger_reac_without_ore(reac):
        for chem in reactions[reac]["chems"]:
            i, c = strip_int(chem)

            if c == "ORE":
                available_chems[reac] = -1
                break

            # Gather lower material if needed
            while available_chems[c] < i:
                if available_chems[c] == -1:
                    if reac == "FUEL":
                        print(available_chems["FUEL"])
                        available_chems["FUEL"] = -1
                    break
                else:
                    trigger_reac(c)

            # When there is enough sub-material, perform reaction
            if available_chems[c] != -1:
                available_chems[c] -= i

        # Append amount to available-dict
        if available_chems[reac] != -1:
            available_chems[reac] += reactions[reac]["amount"]


    with open("input.txt") as f:
        for line in f.readlines():
            components = line.strip().replace(' =>', ',').split(', ')
            i, c = strip_int(components[-1])
            reactions[c] = {"amount": i, "chems": components[:-1]}

    for chem in reactions:
        available_chems[chem] = 0

    trigger_reac("FUEL")

    print("{} ORE used for 1 FUEL".format(used_ore))

    # Part 2
    produced_fuel = 1000000000000 // used_ore

    for chem in available_chems:
        available_chems[chem] *= produced_fuel

    available_chems["FUEL"] = produced_fuel

    print(available_chems["FUEL"])
    while available_chems["FUEL"] != -1:
        trigger_reac_without_ore("FUEL")
        print(available_chems["FUEL"])
    print(available_chems["FUEL"])

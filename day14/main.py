

def strip_int(val):
    # Returns the int part and the material part
    for i in range(len(val)):
        try:
            int(val[i])
        except ValueError:
            return int(val[:i]), val[i+1:]


if __name__ == '__main__':
    used_ore = 0
    created_fuel = 0
    reactions = {}
    available_chems = {}

    def trigger_reac(reac, num):
        global used_ore
        for chem in reactions[reac]["chems"]:
            i, c = strip_int(chem)

            if c == "ORE":
                used_ore += i * num
                break

            # Gather lower material if needed
            while available_chems[c] < i * num:
                trigger_reac(c, num)

            # When there is enough sub-material, perform reaction
            available_chems[c] -= i * num
        # Append amount to available-dict
        available_chems[reac] += reactions[reac]["amount"] * num


    with open("input.txt") as f:
        for line in f.readlines():
            components = line.strip().replace(' =>', ',').split(', ')
            i, c = strip_int(components[-1])
            reactions[c] = {"amount": i, "chems": components[:-1]}

    for chem in reactions:
        available_chems[chem] = 0

    trigger_reac("FUEL", 1)
    created_fuel += 1

    print("{} ORE used for {} FUEL".format(used_ore, created_fuel))

    # Part 2

    max_ore = 1000000000000

    # Coarse calculations
    while used_ore < max_ore * 0.9999:
        trigger_reac("FUEL", 100)
        created_fuel += 100
        percentage = used_ore / max_ore
        print("({}), Created {} fuel with a total of {} ore".format(percentage, created_fuel, used_ore))

    # More fine calculations
    while used_ore < max_ore:
        trigger_reac("FUEL", 1)
        created_fuel += 1
        percentage = used_ore / max_ore
        print("({}), Created {} fuel with a total of {} ore".format(percentage, created_fuel, used_ore))

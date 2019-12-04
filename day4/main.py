
def main():
    low = 172851
    high = 675869
    passwords = 0

    for i in range(low, high+1):
        txt_repr = i.__str__()
        prior_num = int(txt_repr[0])

        two_same = False
        decreasing = True

        for p in txt_repr[1:]:
            if int(p) < prior_num:
                decreasing = False
            if int(p) == prior_num and txt_repr.count(p) == 2:  # Part 2
                two_same = True

            prior_num = int(p)

        if two_same and decreasing:
            passwords += 1

    print("Passwords: " + passwords.__str__())


if __name__ == '__main__':
    main()

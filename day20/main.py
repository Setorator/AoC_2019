import sys




def main1():
    path = set()
    portals = {}

    # Need to increase recursion limit since there is a lot of paths that can be taken
    sys.setrecursionlimit(10**6)

    def dfs(visited, node):
        if node not in visited:
            neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            # Travel across portal
            if node in portals:
                if portals[node] == "ZZ":
                    print("Len: {}".format(len(visited)))
                    print("Path: {}".format(visited))

                for po in portals:
                    if portals[po] == portals[node] and po != node:
                        dfs(visited + [node], po)

            # Travel all neighbours
            for n in neighbours:
                new_node = (node[0] + n[0], node[1] + n[1])
                if new_node in path:
                    dfs(visited + [node], new_node)

    with open("input.txt") as f:
        cave = f.readlines()

        # Add paths
        for y in range(len(cave)):
            for x in range(len(cave[y])):
                if cave[y][x] == ".":
                    path.add((x, y))

        # Add portals
        for y in range(1, len(cave)-1):
            for x in range(1, len(cave[y])-1):
                if cave[y][x].isalpha():
                    if cave[y][x-1].isalpha() and cave[y][x+1] == ".":
                        portals[(x+1, y)] = cave[y][x-1] + cave[y][x]
                    elif cave[y][x+1].isalpha() and cave[y][x-1] == ".":
                        portals[(x-1, y)] = cave[y][x] + cave[y][x+1]

                    elif len(cave[y + 1])-1 >= x and len(cave[y - 1])-1 >= x:
                        if cave[y+1][x].isalpha() and cave[y-1][x] == ".":
                            portals[(x, y-1)] = cave[y][x] + cave[y+1][x]
                        elif cave[y-1][x].isalpha() and cave[y+1][x] == ".":
                            portals[(x, y+1)] = cave[y-1][x] + cave[y][x]

    for p in portals:
        if portals[p] == "AA":
            start = p

    dfs([], start)


if __name__ == '__main__':
    main1()

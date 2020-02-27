'''
Created on 30 Dec 2019

@author: Keith.Gough

NOTE: Solution copied from one of the redit threads https://repl.it/@joningram/AOC-2019


'''

KEYS = 'abcdefghijklmnopqrstuvwxyz'

MAZE = []
with open("day_18_data.txt") as file:
    MAZE = file.readlines()

# pylint: disable=invalid-name

def print_maze():
    """ Print out the maze """
    for line in MAZE:
        print(line.strip())

def find_all_distances(source, data):
    """ Find distances to each door/key from the given start point """
    visited = {source}
    routeinfo = {}
    queue = [(source, 0, "")]

    for (posn, dist, route) in queue:
        contents = data[posn[1]][posn[0]]
        if contents not in ".@#1234" and dist > 0:
            routeinfo[contents] = (dist, route)
            route = route + contents
        visited.add(posn)

        for d in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_posn = (posn[0] + d[0], posn[1] + d[1])
            if data[new_posn[1]][new_posn[0]] != '#' and new_posn not in visited:
                queue.append((new_posn, dist+1, route))

    return routeinfo

def find_routeinfo(data):
    """ Find the route information for all keys/Doors/start points """
    routeinfo = {}
    for y in range(len(data)):
        for x in range(len(data[y])):
            content = data[y][x]
            if content in KEYS + "@1234":
            #if content in "@":
                routeinfo[content] = find_all_distances((x, y), data)
    return routeinfo

def part_one(data):
    """ Find the shortest path to collect all the keys
    """

    routeinfo = find_routeinfo(data)
    keys = frozenset(k for k in routeinfo.keys() if k in KEYS)

    # We use frozensets here because they are immutable therefore
    # can be used as keys for dicts.

    # Route information for each round is a dict mapping
    #   (current location, current keys) -> distance from start
    info = {('@', frozenset()):0}

    for _ in range(len(keys)):
        nextinfo = {}
        for item in info:
            curloc, curkeys, curdist = item[0], item[1], info[item]
            for newkey in keys:
                if newkey not in curkeys:
                    dist, route = routeinfo[curloc][newkey]
                    reachable = all((c in curkeys or c.lower() in curkeys) for c in route)

                    if reachable:
                        newdist = curdist + dist
                        newkeys = frozenset(curkeys | set((newkey,)))

                        if ((newkey, newkeys) not in nextinfo or
                                newdist < nextinfo[(newkey, newkeys)]):

                            nextinfo[(newkey, newkeys)] = newdist

        info = nextinfo

    print("There are", len(info), "final positions.")
    print("Best total distance:", min(info.values()))

def update_for_part_2(data):
    """ Update the maze to split it into 4 quadrants """
    data = [list(line) for line in data]
    for sy in range(len(data)):
        for sx in range(len(data[0])):
            if data[sy][sx] == '@':
                for (dx, dy) in [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]:
                    data[sy+dy][sx+dx] = '#'
                data[sy-1][sx-1] = '1'
                data[sy-1][sx+1] = '2'
                data[sy+1][sx-1] = '3'
                data[sy+1][sx+1] = '4'
                return ["".join(line) for line in data]

def part_two(data):
    """ Run the analysis for 4 robots, one in each quadrant """
    data = update_for_part_2(data)

    routeinfo = find_routeinfo(data)
    keys = frozenset(k for k in routeinfo.keys() if k in KEYS)

    # Each state is now (position of all robots,keys collected) -> distance

    info = {(('1', '2', '3', '4'), frozenset()):0}

    for _ in range(len(keys)):
        nextinfo = {}
        for item in info:
            curlocs, curkeys, curdist = item[0], item[1], info[item]

            for newkey in keys:
                if newkey not in curkeys:
                    for robot in range(4):
                        if newkey in routeinfo[curlocs[robot]]:
                            dist, route = routeinfo[curlocs[robot]][newkey]
                            reachable = all((c in curkeys or c.lower() in curkeys) for c in route)

                            if reachable:
                                newdist = curdist + dist
                                newkeys = frozenset(curkeys | set((newkey,)))
                                newlocs = list(curlocs)
                                newlocs[robot] = newkey
                                newlocs = tuple(newlocs)

                                if ((newlocs, newkeys) not in nextinfo or
                                        newdist < nextinfo[(newlocs, newkeys)]):

                                    nextinfo[(newlocs, newkeys)] = newdist
        info = nextinfo

    print("There are", len(info), "final positions.")
    print("Best total distance:", min(info.values()))

if __name__ == "__main__":
    part_one(MAZE)
    part_two(MAZE)
    #print_maze()

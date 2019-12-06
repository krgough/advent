'''
Created on 6 Dec 2019

@author: Keith.Gough

Advent of Code 2019 - Day 6: Universal Orbit Map


Count number of direct and indirect orbits in the data set.

Data set is a branching tree with a common root (c.f. a file system with directories)
So we can walk the tree (using recursion) to each outer twig node and count each hop
to calculate total number of orbits.

e.g.

        G - H       J - K - YOU
       /           /
COM - B - C - D - E - F
               \
                SAN

COM = Centre of Mass

H orbits G directly and B, COM indirectly.

N = number of hops to the planet
Bn = Number of bodies at layer n

Number of orbits = (B1*1) + (B2*2) + ... + (Bn * N)

'''


TEST_1_RAW = """COM)B
                B)C
                C)D
                D)E
                E)F
                B)G
                G)H
                D)SAN
                E)J
                J)K
                K)YOU
"""

TEST_1 = [orb.strip() for orb in TEST_1_RAW.strip().split('\n')]

def load_file(filename):
    """ load data file """
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append(line.strip())
    return data

def next_level_bodies(bodies, orb_dict):
    """ Return a list of bodies that are at the next level in the tree """
    body_list = []
    for body in bodies:
        if orb_dict[body]:
            body_list += orb_dict[body]
    return body_list

def build_orb_dict(orb_list):
    """ Build the orb dict of lists
        Lists of bodies in direct orbit around any planet
    """
    orb_dict = {}
    for orb in orb_list:
        planet = orb.split(')')[0]
        body = orb.split(')')[1]
        if planet not in orb_dict:
            orb_dict[planet] = [body]
        else:
            orb_dict[planet].append(body)

    # Add in the branch ends
    bodies = [body.split(')')[1] for body in orb_list]
    for body in bodies:
        if body not in orb_dict:
            orb_dict[body] = None
    return orb_dict

def orbit_count(orb_list):
    """ sandbox """

    orb_dict = build_orb_dict(orb_list)

    bods = ['COM']
    level = 1
    orb_count = 0
    while bods:
        bods = next_level_bodies(bods, orb_dict)
        if bods:
            orb_count += level * len(bods)
            level += 1

    return orb_count

def find_key(value, my_dict):
    """ Return the key where the value is stored """
    for key in my_dict:
        if value in my_dict[key]:
            return key
    return None

def backward_route(start_node, end_node, orb_dict):
    """ Find a list moving backward towards COM from start_node """
    route_list = []
    node = start_node
    while node != end_node:
        node = find_key(node, orb_dict)
        route_list.append(node)
    return route_list

def transfer_count(orb_list):
    """ Count orbital transfers between SAN and YOU """
    orb_dict = build_orb_dict(orb_list)

    # Get a list of hops back from SAN to COM and YOU to COM
    san_list = backward_route('SAN', 'COM', orb_dict)
    you_list = backward_route('YOU', 'COM', orb_dict)

    # Find the first common point (JUNC) from end of both lists
    common_ancestor = [body for body in san_list if body in you_list][0]

    # Count hops from SAN to the JUNC, count hops from YOU to JUNK
    san_list = backward_route("SAN", common_ancestor, orb_dict)
    you_list = backward_route("YOU", common_ancestor, orb_dict)

    # Add those and subtract 2
    t_count = len(san_list) + len(you_list) - 2
    return t_count

def main():
    """ Main Program """

    # Tests
    assert orbit_count(TEST_1) == 42
    assert transfer_count(TEST_1) == 3

    # Load data
    data = load_file('day_6_data.txt')

    # Part 1
    print(f"Total number of orbital counts in dataset  = {orbit_count(data)}")

    # Part 2
    print(f"Count of orbital transfers from SAN to YOU = {transfer_count(data)}")

if __name__ == "__main__":
    main()

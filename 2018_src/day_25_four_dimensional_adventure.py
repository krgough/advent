'''
Created on 4 Dec 2019

@author: Keith.Gough

Advent of code 2018 - Day25 Task

'''


TEST_1 = [(0, 0, 0, 0),
          (3, 0, 0, 0),
          (0, 3, 0, 0),
          (0, 0, 3, 0),
          (0, 0, 0, 3),
          (0, 0, 0, 6),
          (9, 0, 0, 0),
          (12, 0, 0, 0)]

TEST_2 = [(-1, 2, 2, 0),
          (0, 0, 2, -2),
          (0, 0, 0, -2),
          (-1, 2, 0, 0),
          (-2, -2, -2, 2),
          (3, 0, 2, -1),
          (-1, 3, 2, 2),
          (-1, 0, -1, 0),
          (0, 2, 1, -2),
          (3, 0, 0, 0)]

TEST_3 = [(1, -1, 0, 1),
          (2, 0, -1, 0),
          (3, 2, -1, 0),
          (0, 0, 3, 1),
          (0, 0, -1, -1),
          (2, 3, -2, 0),
          (-2, 2, 0, 0),
          (2, -2, 0, -1),
          (1, -1, 0, -1),
          (3, 2, 0, 2)]

TEST_4 = [(1, -1, -1, -2),
          (-2, -2, 0, 1),
          (0, 2, 1, 3),
          (-2, 3, -2, 1),
          (0, 2, 3, -2),
          (-1, -1, 1, -2),
          (0, -2, -1, 0),
          (-2, 2, 3, -1),
          (1, 2, 2, 0),
          (-1, -2, 0, -2)]

def load_data(filename):
    """ Load puzzle data from a file """
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append(tuple([int(i) for i in line.strip().split(",")]))
    return data

def find_distance(point1, point2):
    """ Find the manhattan distance between 2 4d points """
    dist = 0
    for i in range(0, 4):
        dist += abs(point2[i] - point1[i])
    return dist

def convert_constellation(constellations, old_const, new_const):
    """ Convert any points marked as members of old_const to be
        marked as members of new_const
    """
    constellations = [new_const if point == old_const else point for point in constellations]
    return constellations

def find_constellations(points, dist):
    """ Two points are in the same constellation if their manhattan distance
        is dist or less.

        For each point:
            Check if any other point is within constellation distance and
            mark those as belonging to constellation x.
            If any found points are already in a constellation y then
            change all y to constellatiom x.

            Think of this as new constellation 'infecting' the old one
            and assimilating all it's points.

    """
    constellations = []
    for i in range(0, len(points)):
        constellations.append(None)

    for new_const, point1 in enumerate(points):
        for i, point2 in enumerate(points):
            m_dist = find_distance(point1, point2)
            if m_dist <= dist:
                old_const = constellations[i]
                if old_const is not None:
                    constellations = convert_constellation(constellations, old_const, new_const)
                constellations[i] = new_const
    return constellations

def count_constellations(points, dist):
    """ Count number of constellations in points.  Points are in the same
        constellation if their Manhattan distance is <= dist to any other
        point.
    """
    return len(set(find_constellations(points, dist)))

def main():
    """ Main Program """

    # Tests

    # Check 4d Manhattan distance calcs
    assert find_distance(TEST_1[0], TEST_1[1]) == 3
    assert find_distance(TEST_1[1], TEST_1[2]) == 6
    assert find_distance(TEST_1[2], TEST_1[3]) == 6
    assert find_distance(TEST_1[3], TEST_1[4]) == 6
    assert find_distance(TEST_1[4], TEST_1[5]) == 3
    assert find_distance(TEST_1[5], TEST_1[6]) == 15
    assert find_distance(TEST_1[6], TEST_1[7]) == 3

    assert count_constellations(TEST_1, 3) == 2
    assert count_constellations(TEST_2, 3) == 4
    assert count_constellations(TEST_3, 3) == 3
    assert count_constellations(TEST_4, 3) == 8

    # Part 1: Count the constellations in the given dataset
    points = load_data("day_25_data.txt")
    dist = 3
    print(f"Part1: Count of constellations in dataset: {count_constellations(points, dist)}")

    print("All done.")
if __name__ == "__main__":
    main()

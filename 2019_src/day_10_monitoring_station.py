'''
Created on 10 Dec 2019

@author: Keith.Gough

Advent of Code 2019 - Day 10: Monitoring Station


Find the point that has a clear line of sight the the maximum
other number of points in a grid.

Possible solutions:

- Find all lines to other points and ignore duplicates
- Find all bearings to other points and ignore duplicates

We want a list of tuples where each tuple contains the x and y
coords of the aseroid at that point.


'''

import math

MAP_DATA = """
###..#.##.####.##..###.#.#..
#..#..###..#.......####.....
#.###.#.##..###.##..#.###.#.
..#.##..##...#.#.###.##.####
.#.##..####...####.###.##...
##...###.#.##.##..###..#..#.
.##..###...#....###.....##.#
#..##...#..#.##..####.....#.
.#..#.######.#..#..####....#
#.##.##......#..#..####.##..
##...#....#.#.##.#..#...##.#
##.####.###...#.##........##
......##.....#.###.##.#.#..#
.###..#####.#..#...#...#.###
..##.###..##.#.##.#.##......
......##.#.#....#..##.#.####
...##..#.#.#.....##.###...##
.#.#..#.#....##..##.#..#.#..
...#..###..##.####.#...#..##
#.#......#.#..##..#...#.#..#
..#.##.#......#.##...#..#.##
#.##..#....#...#.##..#..#..#
#..#.#.#.##..#..#.#.#...##..
.#...#.........#..#....#.#.#
..####.#..#..##.####.#.##.##
.#.######......##..#.#.##.#.
.#....####....###.#.#.#.####
....####...##.#.#...#..#.##.
"""

TEST_MAP_1 = """
.#..#
.....
#####
....#
...##
"""

TEST_MAP_2 = """
.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##
"""

def load_map(map_data):
    """ Takes the raw map input and creates a list of tuples
        representing the co-ordinates for each asteroid '#'
        on the map.
        asteroid = '#'
        empty space = '.'

    """
    points = []
    lines = [line for line in map_data.splitlines() if line != ""]

    for y_coord, line in enumerate(lines):
        line = line.strip()
        for x_coord, point in enumerate(line):
            if point == '#':
                points.append((x_coord, y_coord))
    return points

def bearing_dist(point1, point2):
    """ Returns the bearing from point1 to point 2

        atan2 takes both parameters and works out the correct
        bearing for the quadrant the point is in.

    """
    delta_y = - (point2[1] - point1[1])
    delta_x = point2[0] - point1[0]

    if point1 == point2:
        return None, None
    bearing = (90 - (math.atan2(delta_y, delta_x) * 180 / math.pi)) % 360

    dist = math.sqrt(delta_x**2 + delta_y**2)

    return bearing, dist

def visible(points):
    """ Return a list of dicts containing the visible points from each point

    """
    all_visible = []
    for point1 in points:
        vis = {}
        for point2 in points:
            brg, dist = bearing_dist(point1, point2)
            if brg is not None:
                if brg not in vis:
                    vis[brg] = (dist, point2)
                elif dist < vis[brg][0]:
                    vis[brg] = (dist, point2)
        all_visible.append({'point': point1, 'visible': vis})
    return all_visible

def key_for_max_dict_value(data_dict):
    """  Returns the key for the maximum value in the dict
    """
    vals = list(data_dict.values())
    keys = list(data_dict.keys())
    max_value_key = keys[vals.index(max(vals))]
    return max_value_key

def main():
    """ Main Program """

    points = load_map(MAP_DATA)
    #points = load_map(TEST_MAP_2)

    # Part 1: Find the asteroid with max visibility of other asteroids
    all_visible = visible(points)
    count_visible = {point['point']:len(point['visible']) for point in all_visible}
    max_key = key_for_max_dict_value(count_visible)
    assert max_key == (22, 19)
    assert count_visible[max_key] == 282
    print("Part 1: Base Asteroid with visibility of max other asteroids.")
    print(max_key, count_visible[max_key])

    # Part 2: Zap all asteroids with the rotating laser.
    # Laser rotates from 0-360 and repeats.  It vaporises asteroids
    # as it sweeps over them.  Laser only zaps innermost object
    # on every sweep.  Find the 200th object to get it with the
    # angry photons.

    # List the visible asteriods and copy to the zapped list.
    # Remove zapped objects from our working list.
    # Repeat until the zapped list length gets >= 200.
    #{'0': [point1, point2], 'x': []}
    #print(all_visible)

    print("\nPart 2: 200th Asteroid to be zapped by the laser")
    print("Fire the photon topedoes... moo ha ha")
    vis = [obj for obj in all_visible if obj['point'] == max_key][0]

    obj_bearings = sorted(list(vis['visible'].keys()))
    bearing_to_200th = obj_bearings[199]

    obj_200 = vis['visible'][bearing_to_200th][1]
    print(obj_200, (obj_200[0] * 100) + obj_200[1])

if __name__ == "__main__":
    main()

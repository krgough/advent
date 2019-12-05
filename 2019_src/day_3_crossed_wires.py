#!/usr/bin/env python3
'''
Created on 3 Dec 2019

@author: Keith.Gough

Advent of Code 2019 - Day3 Task

'''

import sys

TEST_1A = ['R8', 'U5', 'L5', 'D3']
TEST_1B = ['U7', 'R6', 'D4', 'L4']
TEST_1 = [TEST_1A, TEST_1B]
TEST_1_RESULT = 6

TEST_2A = ['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72']
TEST_2B = ['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83']
TEST_2 = [TEST_2A, TEST_2B]
TEST_2_RESULT = 159
TEST_2_SHORT_TIME = 610

def load_data(filename):
    """ Load the puzzle data from a file
        Return a list of lists.
        result = [[wire1_data], [wire2_data]]
    """
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append(line.strip().split(','))
    return data

def build_track(data):
    """ Create a list of points for the track of the wire
        Returns a set of tuples, each tuple is a grid co-ord
    """
    track_data = []
    posn = (0, 0)    # Initial position is in the centre of the grid
    for move in data:

        if move.startswith('R'):
            # move right
            x_step = 1
            y_step = 0
        elif move.startswith('L'):
            # move left
            x_step = -1
            y_step = 0
        elif move.startswith('U'):
            # move up
            x_step = 0
            y_step = 1
        elif move.startswith('D'):
            # move down
            x_step = 0
            y_step = -1
        else:
            print("Unexpected move")
            print(f"Move = {move}")
            sys.exit(1)

        dist = int(move[1:])
        for _ in range(1, dist+1):
            posn = posn[0] + x_step, posn[1] + y_step
            track_data.append(posn)
    return track_data

def find_closest_intersections(wire_data):
    """ Find manhatten distance for the intersection point closest to origin """

    # Find the intersection of the two lists
    intersections = find_intersections(wire_data)

    # For each intersection measure distance from the centre
    dists = [abs(point[0]) + abs(point[1]) for point in intersections]

    return min(dists)

def find_intersections(wire_data):
    """ Find all the intersections """
    # Build a set of course points for each wire
    tracks = [build_track(wire) for wire in wire_data]

    # Find the intersection of the two lists
    intersections = list(set(tracks[0]) & set(tracks[1]))
    return intersections

def time_to_position(tracks, point):
    """ Find the time taken (number of steps) to a given point in the track
        Num steps is same as the list index for the point
    """

    index1 = [index for index, track_point in enumerate(tracks[0]) if track_point == point][0]
    index2 = [index for index, track_point in enumerate(tracks[1]) if track_point == point][0]

    # We add one to the length of each track as 0,0 to first point is missing from the track data
    return index1 + 1 + index2 + 1

def find_shortest_time_to_intersect(wire_data):
    """ Find the shortest number of combind steps to an intersection """
    intersections = find_intersections(wire_data)
    tracks = [build_track(wire) for wire in wire_data]

    intersect_times = []
    for i in intersections:
        time_taken = time_to_position(tracks, i)
        intersect_times.append(time_taken)
    return min(intersect_times)

def main():
    """ Main program """

    # Run tests
    assert find_closest_intersections(TEST_1) == TEST_1_RESULT
    assert find_closest_intersections(TEST_2) == TEST_2_RESULT
    assert find_shortest_time_to_intersect(TEST_2) == TEST_2_SHORT_TIME

    # Load the data for each wire into a list
    filename = 'day_3_data.txt'
    wire_data = load_data(filename)

    closest_intersection = find_closest_intersections(wire_data)
    fastest_intersection = find_shortest_time_to_intersect(wire_data)
    print(f"Manhatten distance to closest intersection = {closest_intersection}")
    print(f"Shortest time to intersection              = {fastest_intersection}")

if __name__ == "__main__":
    main()
    print('All done.')

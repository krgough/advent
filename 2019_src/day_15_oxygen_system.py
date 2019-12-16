'''
Created on 15 Dec 2019

@author: Keith.Gough

Adevent of Code 2019 - Day 15: Oxygen System

'''
import logging
import sys
import threading
import time
import int_code_computer as icc


LOGGER = logging.getLogger(__name__)

MAX_X = 41
MAX_Y = 41
INITIAL_POSN = (21, 21)

# pylint: disable=invalid-name, pointless-string-statement

def print_maze(maze, d_posn):
    """ Print out the maze """

    for y in range(MAX_Y):
        for x in range(MAX_X):
            if (x, y) == d_posn:
                print('D', end='')
            elif (x, y) in maze and maze[(x, y)] != ' ':
                print(maze[(x, y)], end='')
            else:
                print(' ', end='')
        print()
def update_maze(maze, direction, output, d_posn):
    """ Update the maze based on the output """
    if direction == 1:
        # North
        x_delta = 0
        y_delta = -1
    elif direction == 2:
        # South
        x_delta = 0
        y_delta = 1
    elif direction == 3:
        # West
        x_delta = -1
        y_delta = 0
    elif direction == 4:
        # East
        x_delta = 1
        y_delta = 0

    if output == 0:
        # We are against a wall so put a wall in the maze in the
        # relevant direction.
        maze[(d_posn[0] + x_delta, d_posn[1] + y_delta)] = '#'

    elif output == 1:
        # We moved so update the droid position
        new_posn = (d_posn[0] + x_delta, d_posn[1] + y_delta)

        if new_posn in maze and maze[new_posn] != '':
            print(f'ERROR. Position = {maze[new_posn]}')
            sys.exit()
        d_posn = new_posn

    elif output == 2:
        # We found the oxygen system so add make a note of that and move the droid
        maze[(d_posn[0] + x_delta, d_posn[1] + y_delta)] = 'S'
        d_posn = (d_posn[0] + x_delta, d_posn[1] + y_delta)

    return d_posn
def build_maze():
    # pylint: disable=too-many-branches
    """ Run the maze and print out the walls
    """

    program = icc.load_data("day_15.txt")

    # Start a thread here to run the computer
    comp = icc.IntCodeComputer(program)
    comp_thread = threading.Thread(target=comp.run_program)
    comp_thread.daemon = True
    comp_thread.start()

    maze = {}
    d_posn = INITIAL_POSN
    direction = 1
    s_found = False
    all_done = False

    # Make the first move
    comp.input.put(direction)
    while not comp.waiting:
        time.sleep(0.1)

    while not all_done:

        while not comp.output.empty():
            out = comp.output.get()
            d_posn = update_maze(maze, direction, out, d_posn)

            # Keep left hand on the wall
            if out == 0:
                if direction == 1:
                    direction = 4
                elif direction == 2:
                    direction = 3
                elif direction == 3:
                    direction = 1
                elif direction == 4:
                    direction = 2
            elif out == 1:
                if direction == 1:
                    direction = 3
                elif direction == 2:
                    direction = 4
                elif direction == 3:
                    direction = 2
                elif direction == 4:
                    direction = 1
            elif out == 2:
                s_found = True

            comp.input.put(direction)

        if s_found is True and d_posn == INITIAL_POSN:
            all_done = True

    print_maze(maze, d_posn)
    #min_x = min([x[0] for x in maze])
    #max_x = max([x[0] for x in maze])

    #min_y = min([x[1] for x in maze])
    #max_y = max([x[1] for x in maze])

    #print(min_x, min_y)
    #print(max_x, max_y)

    return maze

""" Part 2 Functions """
def build_maze_matrix(maze):
    """ Return a 2-D array for the maze where
        1 = empty
        0 = Wall
    """

    matrix = [[1 for _ in range(MAX_X)] for _ in range(MAX_Y)]

    for y in range(MAX_Y):
        for x in range(MAX_X):
            if (x, y) in maze and maze[(x, y)] == '#':
                matrix[x][y] = 0

#     for y in range(MAX_Y):
#         for x in range(MAX_X):
#             print(matrix[x][y], end='')
#         print()
    return matrix
def can_move(matrix, visited, x, y):
    """ Returns False is dest is a wall or if we have been here previously """
    if matrix[x][y] == 0 or visited[x][y]:
        return False
    return True
def is_valid(x, y):
    """ Check coo-ordinates are valid """
    if 0 <= x < MAX_X and 0 <= y < MAX_Y:
        return True
    return False
def shortest_route(matrix, visited, i, j, x, y, min_dist, dist):
    """ Find shortest route to destinatoin from source

        source = (i, j)
        dest = (x, y)

    """
    # If destination is found the update minimum distance
    if i == x and j == y:
        min_dist = min(dist, min_dist)
        return min_dist

    # Mark the cell as 'visited'
    visited[i][j] = 1

    # Now recursivley move N,S,E,W to each possible new position

    # North
    if is_valid(i, j-1) and can_move(matrix, visited, i, j-1):
        min_dist = shortest_route(matrix, visited, i, j-1, x, y, min_dist, dist+1)

    # South
    if is_valid(i, j+1) and can_move(matrix, visited, i, j+1):
        min_dist = shortest_route(matrix, visited, i, j+1, x, y, min_dist, dist+1)

    # East
    if is_valid(i+1, j) and can_move(matrix, visited, i+1, j):
        min_dist = shortest_route(matrix, visited, i+1, j, x, y, min_dist, dist+1)

    # West
    if is_valid(i-1, j) and can_move(matrix, visited, i-1, j):
        min_dist = shortest_route(matrix, visited, i-1, j, x, y, min_dist, dist+1)

    # Remove the visited route as we exit from the recursive calls
    visited[i][j] = 0

    return min_dist
def find_position(maze, item):
    """ Find position of item in the maze
        Return the x,y coords
    """
    for y in range(MAX_Y):
        for x in range(MAX_X):
            if (x, y) in maze and maze[(x, y)] == item:
                return x, y
    return None, None

def main():
    """ Main Program """

    print("Part 1:")
    print("Mapping the maze...")
    maze = build_maze()

    print("\nFinding shortest route to oxygen system...")
    matrix = build_maze_matrix(maze)
    visited = [[0 for _ in range(MAX_X)] for _ in range(MAX_Y)]

    # i,j = Droid Position
    # x,y = oxygen source position

    (i, j) = INITIAL_POSN
    x, y = find_position(maze, 'S')

    route_len = shortest_route(matrix, visited, i, j, x, y, 9999, 0)
    print(f"Shortest route length = {route_len}")

    print("\nPart 2:")
    print("Finding longest route...")
    route_lengths = []
    for j in range(1, MAX_Y-1):
        for i in range(1, MAX_X-1):
            dist = shortest_route(matrix, visited, i, j, x, y, 9999, 0)
            if dist != 9999:
                route_lengths.append(dist)

    print(f"Maximum time = {max(route_lengths)}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

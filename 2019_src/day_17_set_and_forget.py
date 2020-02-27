'''
Created on 17 Dec 2019

@author: Keith.Gough

Advent of Code 2019 - Day 17: Set and Forget

'''
import threading
import logging
import int_code_computer as icc

LOGGER = logging.getLogger(__name__)

MAX_X = 55 # 0-54
MAX_Y = 53 # 0-52

def build_maze(maze_data):
    # pylint: disable=invalid-name
    """ Build a 2d matrix for the maze """

    maze_data = [chr(val) for val in maze_data if val != 10]
    maze = [['W' for _ in range(MAX_Y)] for _ in range(MAX_X)]

    for i, val in enumerate(maze_data):
        y, x = divmod(i, MAX_X)
        maze[x][y] = val

    return maze
def find_crossings(maze):
    # pylint: disable=invalid-name
    """ Find the crossing points
        Crossings can only be 1 in from the edge

    """
    crossings = []
    for y in range(1, MAX_Y-1):
        for x in range(1, MAX_X-1):
            if (maze[x-1][y] == '#' and maze[x+1][y] == '#' and
                    maze[x][y+1] == '#' and maze[x][y-1] == '#' and
                    maze[x][y] == '#'):

                maze[x][y] = 'O'
                crossings.append((x, y))

    return crossings
def sum_alignments(crossing_points):
    """ Add the coords of the crossing points """
    return sum([point[0] * point[1] for point in crossing_points])

def print_maze(maze):
    # pylint: disable=invalid-name
    """ Print the maze """
    for y in range(MAX_Y):
        for x in range(MAX_X):
            print(maze[x][y], end='')
        print()
def build_movement_function(m_str):
    """ Build the movement function in ASCII from the
        given string of the form:

        'L10, L8, R8, L8, R6'
    """
    m_str = [chars.strip() for chars in m_str.split(',')]

    func = []
    for chars in m_str:
        turn = ord(chars[0])
        func += [turn, ord(',')]

        for char in list(chars[1:]):
            func += [ord(char)]
        func += [ord(',')]

    func[-1] = ord('\n')

    return func
def build_instructions():
    """ Build the move instructions """

    mmr = ['A', 'A', 'B', 'C', 'B', 'C', 'B', 'C', 'B', 'A']

    func_mmr = []
    for char in mmr:
        func_mmr += [ord(char), ord(',')]
    func_mmr[-1] = ord('\n')

    #a_str = 'L10, L8, R8, L8, R6'
    #b_str = 'R6, R6, L8, L10, R6'
    #c_str = 'R8, R8'

    a_str = 'L10, L8, R8, L8, R6'
    b_str = 'R6, R8, R8'
    c_str = 'R6, R6, L8, L10'

    func_a = build_movement_function(a_str)
    func_b = build_movement_function(b_str)
    func_c = build_movement_function(c_str)

    print(func_mmr)
    print(func_a, len(func_a))
    print(func_b, len(func_b))
    print(func_c, len(func_c))

    return func_mmr + func_a + func_b + func_c

def main():
    """ Main Program """
    print('Part 1:')
    program = icc.load_data('day_17_data.txt')
    comp = icc.IntCodeComputer(program)
    comp.run_program()

    maze_raw = []
    while not comp.output.empty():
        maze_raw.append(comp.output.get())

    maze = build_maze(maze_raw)
    crossings = find_crossings(maze)
    print_maze(maze)
    print(f"\nAlignment sum = {sum_alignments(crossings)}")

    print('\nPart 2:')
    program = icc.load_data('day_17_data.txt')
    program[0] = 2 # Wake up the robot
    comp = icc.IntCodeComputer(program)

    # Load the movement instructions
    for ins in build_instructions():
        comp.input.put(ins)

    # Load the y/n for video feed
    comp.input.put(ord('n'))
    comp.input.put(ord('\n'))

    comp_thread = threading.Thread(target=comp.run_program)
    comp_thread.daemon = True
    comp_thread.start()

    output = []
    while True:
        out = comp.output.get()
        output.append(out)
        try:
            print(chr(out), end='')
        except ValueError:
            print(out)
            break

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

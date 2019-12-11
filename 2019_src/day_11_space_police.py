'''
Created on 11 Dec 2019

@author: Keith.Gough

Advent of Code - Day 11: Space Police

IntCode comp give instructions on how to move and what colour to paint
the current location.
Input = colour of current location.
Output = colour to paint the given location, dicection to turn.
We shall paint, turn and then move 1 space.
Need to keep track of pointing dirn

We should count the number of painted spaces (add points to a list and count)
Need to remove duplicates (do not count spaces painted twice)


'''
import threading
import logging
import int_code_computer as icc

LOGGER = logging.getLogger(__name__)

def turn_move(turn_direction, coords, heading):
    """ Calculate new position based on the given turn + move instruction.

        0 = turn left and move 1
        1 = turn right and move 1
    """
    if turn_direction == 0:
        heading = (heading - 90) % 360
    else:
        heading = (heading + 90) % 360

    if heading == 0:
        coords = (coords[0], coords[1] + 1)
    elif heading == 90:
        coords = (coords[0] + 1, coords[1])
    elif heading == 180:
        coords = (coords[0], coords[1] -1)
    elif heading == 270:
        coords = (coords[0] -1 , coords[1])

    #print(coords, heading)
    return coords, heading

def print_sign(painted):
    """ Print out the painted sign

        Our staring location was (0, 0) and we can move in any direction.
        Work out the min x and max y  to find top left of display area

    """
    min_x = min([point[0] for point in painted])
    max_y = max([point[1] for point in painted])

    p_new = {(point[0] - min_x, max_y - point[1]):painted[point] for point in painted}

    max_x = max([point[0] for point in p_new])
    max_y = max([point[1] for point in p_new])

    for y in range(max_y+1):
        for x in range(max_x+1):
            char = p_new.get((x,y), ' ')
            if char == 0:
                char = ' '
            print(char, end='')
        print()

def paint_sign(program):
    """ Run the intCode computer with the given painting program
        Give 0 as initial input then paint, move and give next input.
        Next imput is the colour we have painted the square or if
        not painted then we return black by default.

        0 = Black
        1 = White

    """
    # Dict with keys of tuples for painted squares
    # Values = colour of paint
    # {(x1,y1): c1, (x2, y2):c2  ...}
    initial_colour = 1
    painted = {(0,0):1}

    # Start a thread here to run the computer
    comp = icc.IntCodeComputer(program, [initial_colour])
    comp_thread = threading.Thread(target=comp.run_program)
    comp_thread.daemon = True
    comp_thread.start()

    # Setup initial position
    coords = (0, 0)
    heading = 0

    while not comp.halt_status:
        # Get paint colour
        paint_colour = comp.output.get()
        turn_direction = comp.output.get()
        #print(f"Paint= {paint_colour}, Turn= {turn_direction}")

        # Paint the square (overwrites any existing paint in the square)
        painted[coords] = paint_colour

        # Execute instructed move
        coords, heading = turn_move(turn_direction, coords, heading)

        # Get input for new square
        inp = painted.get(coords, 0)
        comp.input.put(inp)

    return painted

def main():
    """ Main Program """
    # Test turn move
    coords, heading = turn_move(0, (0,0), 0)
    coords, heading = turn_move(0, coords, heading)
    coords, heading = turn_move(0, coords, heading)
    coords, heading = turn_move(0, coords, heading)
    coords, heading = turn_move(1, coords, heading)
    coords, heading = turn_move(1, coords, heading)
    coords, heading = turn_move(1, coords, heading)
    assert turn_move(1, coords, heading) == ((0,0), 0)

    filename = 'day_11_data.txt'
    program = icc.load_data(filename)
    painted = paint_sign(program)

    print(f'Part1: Number of painted squares = {len(painted)}')
    print(f'\nPart 2: Registration Number\n')
    print_sign(painted)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

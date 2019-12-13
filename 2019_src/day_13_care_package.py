'''
Created on 13 Dec 2019

@author: Keith.Gough

Advent of Code 2019 - Day 13: Care Package 

'''
import logging
import threading
import time
import int_code_computer as icc

X_COLS = 37
Y_ROWS = 24
CURSOR_ROW = 22

LOGGER = logging.getLogger(__name__)

def update_grid(comp, grid):
    """ The 2-D array grid with the screen data
    """
    while not comp.waiting and not comp.halt_status:
        time.sleep(0.001)

    while not comp.output.empty():
        # Get 3 results
        x = comp.output.get()
        y = comp.output.get()
        b = comp.output.get()

        if x == -1 and y == 0:
            print(f"Score = {b}")

        grid[x][y] = b

def print_grid(grid):
    """ Print the grid
    """
    for y in range(Y_ROWS):
        for x in range(X_COLS):
            if grid[x][y] == 0:
                print(" ", end='')
            elif grid[x][y] == 1:
                print("|", end='')
            elif grid[x][y] == 2:
                print("#", end='')
            elif grid[x][y] == 3:
                print("^", end='')
            elif grid[x][y] == 4:
                print("0", end='')
        print()

def find_ball(grid):
    """ Find the paddle and ball x-coords and try to close
        the gap between them
    """
    for y in range(Y_ROWS):
        for x in range(X_COLS):
            if grid[x][y] == 4:
                ball_x = x

    return ball_x

def find_paddle(grid):
    """ Find the paddle and ball x-coords and try to close
        the gap between them
    """
    for x in range(X_COLS):
        if grid[x][CURSOR_ROW] == 3:
            paddle_x = x

    return paddle_x

def part_1():
    """ Part 1: Count bricks left at the end
    """

    program = icc.load_data('day_13_data.txt')
    comp = icc.IntCodeComputer(program)
    comp.run_program()

    # Build an empty grid
    grid = [['' for _ in range(24)] for _ in range(37)]

    update_grid(comp, grid)
    print_grid(grid)
    blocks_left = sum([row.count(2) for row in grid])
    print(f"Part1: Blocks left = {blocks_left}")

def part_2():
    """ Part 2: Play the game until no blocks left.
    """
    program = icc.load_data('day_13_data.txt')

    # 2 = Free play
    program[0] = 2

    # Start a thread here to run the computer
    comp = icc.IntCodeComputer(program)
    comp_thread = threading.Thread(target=comp.run_program)
    comp_thread.daemon = True
    comp_thread.start()

    # Build an empty grid
    grid = [['' for _ in range(24)] for _ in range(37)]

    # Run the computer and cature the next grid iteration
    # Apply an input to move the paddle for the next step.
    update_grid(comp, grid)
    last_ball_x = find_ball(grid)
    print_grid(grid)
    comp.input.put(-1)

    while not comp.halt_status:
        if not comp.output.empty():
            update_grid(comp, grid)
            print_grid(grid)
            ball_x = find_ball(grid)

            paddle_x = find_paddle(grid)
            moves = abs(paddle_x - ball_x)
            if moves != 0:
                for _ in range(moves):
                    if ball_x > last_ball_x:
                        comp.input.put(1)
                    else:
                        comp.input.put(-1)
            else:
                comp.input.put(0)

            last_ball_x = ball_x

    print("GAME OVER")

def main():
    """ Main Program """

    part_1()
    part_2()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

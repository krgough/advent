'''
Created on 7 Jan 2020

@author: Keith.Gough


Advent of Code 2019 - Day 19: Tractor Beam

'''
import logging
import sys
import int_code_computer as icc

LOGGER = logging.getLogger(__name__)

BOX_SIZE = 100

# pylint: disable=invalid-name

def get_beam(x, y, prog):
    """ Get the beam value at the given co-ords """
    input_data = [x, y]
    comp = icc.IntCodeComputer(prog, input_data)
    comp.run_program()
    return comp.output.get()

def part_1():
    """ Count beam locations in first 50x50 grid """
    prog = icc.load_data('day_19_data.txt')

    beam_count = 0
    for y in range(0, 50):
        for x in range(0, 50):

            beam = get_beam(x, y, prog)
            beam_count += beam

            print(f'{beam}', end='')
        print()

    print("\nPart1:")
    print(f"Beam count in first 50x50 = {beam_count}")

def check_top_right(x, y, prog):
    """ Check if x + 99 is also in the beam """
    return get_beam(x + (BOX_SIZE - 1), y - (BOX_SIZE - 1), prog)

def find_beam_edge(y, prog, last_edge):
    """ Find the x co-ord of the beam edge """
    x = last_edge - 1
    while x < 5000:
        x += 1
        beam = get_beam(x, y, prog)
        if beam == 1:
            return x
    return None

def part_2():
    """ Find closest distance for a 100x100 object to be fully inside the beam """
    prog = icc.load_data('day_19_data.txt')
    last_edge = 0

    for y in range(100, 5000):
        beam_edge = find_beam_edge(y, prog, last_edge)

        if beam_edge:
            last_edge = beam_edge
            # Check if the top left is inside the beam
            if check_top_right(beam_edge, y, prog):
                print("\nPart 2: Top Left corner of 100x100 box contained by beam: ")
                print(beam_edge, y - (BOX_SIZE - 1))
                print((beam_edge * 10000) + y - (BOX_SIZE - 1))
                sys.exit()
    print("All done")

def main():
    """ Main Program """
    part_1()
    part_2()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

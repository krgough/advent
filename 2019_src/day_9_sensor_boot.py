'''
Created on 9 Dec 2019

@author: Keith.Gough


Advent of Code 2019 - Day 9: Sensor Boost

Add relative mode to intOp computer
    Modify esiting module to include the new addressing mode
    mode 2 = relative mode (addresses are relative to rel_base e.g add = arg + rel_base)
    opCode 9: adjust relative_base.  Takes one argument, which is the new relative_base value

Add arbitrary memory size to intOp computer
    Change prog memory from List to Dict.
    Any new memory location write will create a new key at the given address
    Memory reads should return 0 by default if the location does not already exist.

'''
import logging
import int_code_computer as icc


def main():
    """ Main Program """
    program = icc.load_data('day_9_data.txt')

    print("Part 1: Boost keycode:")
    input_data = [1]
    print(icc.run_computer(program, input_data))

    print("\nPart 2: Distress signal co-ords:")
    input_data = [2]
    print(icc.run_computer(program, input_data))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

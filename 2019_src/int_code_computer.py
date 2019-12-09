'''
Created on 7 Dec 2019

@author: Keith.Gough

Advent of Code 2019

Class module for intcode computer

Making this a class since it seems we will be re-using it for other puzzles

09/12/2019 Keith Gough
Changed program memory to use a Dict rather than a list.
key = address, val = memory contents of 'key' location.
This means we can set arbitrary memory locations to simulate storing data at some
extended memory positions.

Added relative mode to intOp computer
Modify esiting module to include the new addressing mode
mode 2 = relative mode (addresses are relative to rel_base e.g add = arg + rel_base)
opCode 9: adjust relative_base.  Takes one argument, which is the new relative_base value

'''

import queue
import logging

LOGGER = logging.getLogger(__name__)

# Immediate_mode or position_mode
I_MODE = 1
P_MODE = 0
R_MODE = 2

AC_UNIT_ID = 1
TRC_UNIT_ID = 5


# Test 1,2 give output 0 if input 0 and output 1 if input 1
TEST_1 = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9] # Jump test - Position mode
TEST_2 = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]         # Jump test - Immediate mode

# Gives output 999 if input < 8. 1000 if ip == 8, 1001 if ip > 8
TEST_3 = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
          1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
          999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]

# Test uses relative mode addressing
TEST_4 = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]

# Test 5 - generates a large 16 digit number
TEST_5 = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]

# Test 6 - Outputs the large number in the middle
TEST_6 = [104, 1125899906842624, 99]


def load_data(filename):
    """ Load the mass data file """
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data = [int(i) for i in line.strip().split(',')]

    return data

class IntCodeComputer():
    """ Class for managing int code computers """
    def __init__(self, program, input_data=None, output_data=None):

        # Copy the list here so that we have a local copy
        self.program = dict(enumerate(program))
        self.instruction_pointer = 0
        self.relative_base = 0

        if isinstance(input_data, queue.Queue):
            self.input = input_data
        else:
            self.input = queue.Queue()
            if input_data is None:
                input_data = []
            for inp in input_data:
                self.input.put(inp)

        if isinstance(output_data, queue.Queue):
            self.output = output_data
        else:
            self.output = queue.Queue()

        self.halt_status = False
        self.result = []

    def get_arg(self, pointer, address_mode):
        """ Get the argument from either the immediate value or from the location
            pointed to (position mode, relative mode)
        """
        if address_mode == I_MODE:
            arg = self.program.get(pointer, 0)
        elif address_mode == P_MODE:
            arg = self.program.get(self.program.get(pointer, 0), 0)
        elif address_mode == R_MODE:
            arg = self.program.get(self.relative_base + self.program.get(pointer, 0), 0)

        return arg

    def get_result_address(self, pointer, address_mode):
        """ Get the appropriate result address depending on the address mode
        """
        if address_mode == P_MODE:
            result_address = self.program.get(pointer, 0)
        elif address_mode == R_MODE:
            result_address = self.program.get(pointer, 0) + self.relative_base
        else:
            result_address = None
        return result_address

    def process_instruction(self):
        """ Process the instruction at the given index

            Op-code format:

            ABCDE 0 0 0
            ||||| | | |
            ||||| | | Arg 3 (output)
            ||||| | |
            ||||| | Arg 2
            ||||| |
            ||||| Arg 1
            |||||
            ||| 2-Digit op-code
            |||
            ||Arg1 - address mode
            ||
            |Arg2 - address mode
            |
            Arg3 - address mode

            01 = Add, size = 4 fields
            02 = Multiply, size = 4 fields
            03 = Input - take input and store it at location, size = 2 fields
            04 = Output, size = 2 fields
            05 = Jump If True. Size = 3 fields
            06 = Jump if False. Size = 3 fields
            07 = Less than.  Size = 4 fields
            08 = Equals.  Size = 4 fields
            09 = Set relative base

            Pad the op-code with zeros to make it 5 chars

        """
        full_op_code = str(self.program.get(self.instruction_pointer, 0)).zfill(5)
        op_code = full_op_code[-2:]

        LOGGER.debug((self.instruction_pointer, op_code))

        self.halt_status = False
        exit_reason = ''

        if op_code == '99':
            exit_reason = 'Halt OP code.  Halting.'
            self.halt_status = True
            LOGGER.debug(exit_reason)

        elif op_code in ['01', '02', '03', '04', '05', '06', '07', '08', '09']:
            # Either Mode 0 or Mode 1 so here we use the function to always return the value
            arg1 = self.get_arg(self.instruction_pointer + 1, int(full_op_code[2]))
            arg2 = self.get_arg(self.instruction_pointer + 2, int(full_op_code[1]))
            result_address = self.get_result_address(self.instruction_pointer + 3,
                                                     int(full_op_code[0]))

            # Add
            if op_code == '01':
                self.program[result_address] = arg1 + arg2
                self.instruction_pointer += 4

            # Multiply
            elif op_code == '02':
                self.program[result_address] = arg1 * arg2
                self.instruction_pointer += 4

            # Input
            elif op_code == '03':
                # Input uses arg 1 for result address so re-calc the result address
                result_address = self.get_result_address(self.instruction_pointer + 1,
                                                         int(full_op_code[2]))
                self.program[result_address] = self.input.get()
                LOGGER.debug(self.program.get(result_address, 0))
                self.instruction_pointer += 2

            # Output
            elif op_code == '04':
                self.output.put(arg1)
                self.result.append(arg1)
                LOGGER.debug(arg1)
                self.instruction_pointer += 2

            # Jump if true
            elif op_code == '05':
                self.instruction_pointer = arg2 if arg1 else self.instruction_pointer + 3

            # Jump if false
            elif op_code == '06':
                self.instruction_pointer = arg2 if arg1 == 0 else self.instruction_pointer + 3

            # Less than
            elif op_code == '07':
                self.program[result_address] = 1 if arg1 < arg2 else 0
                self.instruction_pointer += 4

            # Equals
            elif op_code == '08':
                self.program[result_address] = 1 if arg1 == arg2 else 0
                self.instruction_pointer += 4

            # Adjust relative mode base
            elif op_code == '09':
                self.relative_base = self.relative_base + arg1
                self.instruction_pointer += 2

        else:
            exit_reason = 'Unknown op_code. Halting operation.'
            self.halt_status = True
            LOGGER.debug(exit_reason)

    def run_program(self):
        """ Run the given program """
        self.instruction_pointer = 0

        while not self.halt_status:
            self.process_instruction()

def run_computer(program, input_data):
    """ run basic int code computer tests """

    # Build and run the computer.
    comp = IntCodeComputer(program, input_data)
    comp.run_program()
    return comp.result

def run_tests():
    """ Run test programs """

    # Tests
    assert run_computer(TEST_1, [0]) == [0]
    assert run_computer(TEST_1, [1]) == [1]
    assert run_computer(TEST_2, [0]) == [0]
    assert run_computer(TEST_2, [1]) == [1]
    assert run_computer(TEST_3, [7]) == [999]
    assert run_computer(TEST_3, [8]) == [1000]
    assert run_computer(TEST_3, [9]) == [1001]
    assert run_computer(TEST_4, None) == TEST_4

    assert run_computer(TEST_5, None) == [1219070632396864]
    assert run_computer(TEST_6, None) == [1125899906842624]

    program = load_data('day_5_data.txt')
    assert run_computer(program, input_data=[AC_UNIT_ID]) == [0, 0, 0, 0, 0, 0, 0, 0, 0, 6761139]
    assert run_computer(program, input_data=[TRC_UNIT_ID]) == [9217546]


    LOGGER.info('Instruction Computer: all tests pass')

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run_tests()

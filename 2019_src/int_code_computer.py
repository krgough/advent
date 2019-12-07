'''
Created on 7 Dec 2019

@author: Keith.Gough

Advent of Code 2019

Class module for intcode computer

Making this a class since it seems we will be re-using it for other puzzles


'''

import queue
import logging

LOGGER = logging.getLogger(__name__)

# Immediate_mode or position_mode
I_MODE = 1
P_MODE = 0

AC_UNIT_ID = 1
TRC_UNIT_ID = 5


# Test 1,2 give output 0 if input 0 and output 1 if input 1
TEST_1 = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9] # Jump test - Position mode
TEST_2 = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]         # Jump test - Immediate mode

# Gives output 999 if input < 8. 1000 if ip == 8, 1001 if ip > 8
TEST_3 = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
          1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
          999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]

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
        self.program = list(program)
        self.instruction_pointer = 0

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
        """ Get the argument from either the pointer (immediate mode) or from
            memory location with addr stored at pointer.
        """
        if address_mode == I_MODE:
            arg = self.program[pointer]
        else:
            arg = self.program[self.program[pointer]]
        return arg

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

            Pad the op-code with zeros to make it 5 chars

        """
        full_op_code = str(self.program[self.instruction_pointer]).zfill(5)
        op_code = full_op_code[-2:]

        LOGGER.debug((self.instruction_pointer, op_code))

        self.halt_status = False
        exit_reason = ''

        if op_code == '99':
            exit_reason = 'Halt OP code.  Halting.'
            self.halt_status = True

        elif op_code in ['01', '02', '05', '06', '07', '08']:
            # Either Mode 0 or Mode 1 so here we use the function to always return the value
            arg1 = self.get_arg(self.instruction_pointer + 1, int(full_op_code[2]))
            arg2 = self.get_arg(self.instruction_pointer + 2, int(full_op_code[1]))
            result_address = self.program[self.instruction_pointer + 3]

            # Add
            if op_code == '01':
                self.program[result_address] = arg1 + arg2
                self.instruction_pointer += 4

            # Multiply
            elif op_code == '02':
                self.program[result_address] = arg1 * arg2
                self.instruction_pointer += 4

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

        # Input
        elif op_code == '03':
            # Always mode 0 - so here we always read an address not a value
            result_address = self.program[self.instruction_pointer + 1]
            self.program[result_address] = self.input.get()
            LOGGER.debug(self.program[result_address])
            self.instruction_pointer += 2

        # Output
        elif op_code == '04':
            # Either Mode 0 or Mode 1 so here we use the function to always return the value
            arg1 = self.get_arg(self.instruction_pointer + 1, int(full_op_code[2]))
            #print(arg1)
            self.output.put(arg1)
            self.result.append(arg1)
            LOGGER.debug(arg1)
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

    program = load_data('day_5_data.txt')
    assert run_computer(program, input_data=[AC_UNIT_ID]) == [0, 0, 0, 0, 0, 0, 0, 0, 0, 6761139]
    assert run_computer(program, input_data=[TRC_UNIT_ID]) == [9217546]

    LOGGER.info('Instruction Computer: all tests pass')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_tests()

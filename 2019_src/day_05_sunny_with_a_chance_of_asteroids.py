'''
Created on 5 Dec 2019

@author: Keith.Gough

Advent of Code 2019 - Day5 Task

'''

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

def get_arg(pointer, address_mode, program):
    """ Get the argument from either the pointer (immediate mode) or from
        memory location with addr stored at pointer.
    """
    if address_mode == I_MODE:
        arg = program[pointer]
    else:
        arg = program[program[pointer]]
    return arg

def process_instruction(instruction_pointer, program, input_data):
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

    halt_program = False
    output = None

    full_op_code = str(program[instruction_pointer]).zfill(5)
    op_code = full_op_code[-2:]

    if op_code == '99':
        halt_program = True

    elif op_code in ['01', '02', '05', '06', '07', '08']:
        # Either Mode 0 or Mode 1 so here we use the function to always return the value
        arg1 = get_arg(instruction_pointer + 1, int(full_op_code[2]), program)
        arg2 = get_arg(instruction_pointer + 2, int(full_op_code[1]), program)
        result_address = program[instruction_pointer + 3]

        # Add
        if op_code == '01':
            program[result_address] = arg1 + arg2
            instruction_pointer += 4

        # Multiply
        elif op_code == '02':
            program[result_address] = arg1 * arg2
            instruction_pointer += 4

        # Jump if true
        elif op_code == '05':
            instruction_pointer = arg2 if arg1 else instruction_pointer + 3

        # Jump if false
        elif op_code == '06':
            instruction_pointer = arg2 if arg1 == 0 else instruction_pointer + 3

        # Less than
        elif op_code == '07':
            program[result_address] = 1 if arg1 < arg2 else 0
            instruction_pointer += 4

        # Equals
        elif op_code == '08':
            program[result_address] = 1 if arg1 == arg2 else 0
            instruction_pointer += 4

    elif op_code == '03':
        # Always mode 0 - so here we always read an address not a value
        result_address = program[instruction_pointer + 1]
        program[result_address] = input_data
        instruction_pointer += 2

    elif op_code == '04':
        # Either Mode 0 or Mode 1 so here we use the function to always return the value
        arg1 = get_arg(instruction_pointer + 1, int(full_op_code[2]), program)
        #print(arg1)
        output = arg1
        instruction_pointer += 2

    else:
        print('Unknown op_code. Halting operation.')
        halt_program = True

    return halt_program, instruction_pointer, output

def run_program(program, input_data):
    """ Run the given program """
    halt = False
    instruction_pointer = 0
    result = []

    while not halt:
        halt, instruction_pointer, output = process_instruction(instruction_pointer,
                                                                program,
                                                                input_data)
        if output is not None:
            result.append(output)
    return result

def main():
    """ Main Program """

    # Tests
    assert run_program(list(TEST_1), 0)[-1] == 0
    assert run_program(list(TEST_1), 1)[-1] == 1
    assert run_program(list(TEST_2), 0)[-1] == 0
    assert run_program(list(TEST_2), 1)[-1] == 1
    assert run_program(list(TEST_3), 7)[-1] == 999
    assert run_program(list(TEST_3), 8)[-1] == 1000
    assert run_program(list(TEST_3), 9)[-1] == 1001

    # Part1
    program = load_data('day_05_data.txt')
    result = run_program(program, input_data=AC_UNIT_ID)
    print(f"Diagnostic code for system ID {AC_UNIT_ID}: {result}")

    # Part2
    program = load_data('day_05_data.txt')
    result = run_program(program, input_data=TRC_UNIT_ID)
    print(f"\nDiagnostic code for system ID {TRC_UNIT_ID}: {result}")

if __name__ == "__main__":
    main()

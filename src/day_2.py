'''
Created on 2 Dec 2019

@author: Keith.Gough

Advent of Code 2019 - Day2 Task

'''

TEST_1 = [1,0,0,0,99]
TEST_1_RESULT = [2,0,0,0,99]

TEST_2 = [2,3,0,3,99]
TEST_2_RESULT = [2,3,0,6,99]

TEST_3 = [2,4,4,5,99,0]
TEST_3_RESULT = [2,4,4,5,99,9801]

TEST_4 = [1,1,1,4,99,5,6,0,99]
TEST_4_RESULT = [30,1,1,4,2,5,6,0,99]

PROGRAM = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,9,19,1,19,5,23,1,13,23,27,
           1,27,6,31,2,31,6,35,2,6,35,39,1,39,5,43,1,13,43,47,1,6,47,51,2,
           13,51,55,1,10,55,59,1,59,5,63,1,10,63,67,1,67,5,71,1,71,10,75,1,
           9,75,79,2,13,79,83,1,9,83,87,2,87,13,91,1,10,91,95,1,95,9,99,1,
           13,99,103,2,103,13,107,1,107,10,111,2,10,111,115,1,115,9,119,2,
           119,6,123,1,5,123,127,1,5,127,131,1,10,131,135,1,135,6,139,1,10,
           139,143,1,143,6,147,2,147,13,151,1,5,151,155,1,155,5,159,1,159,2,
           163,1,163,9,0,99,2,14,0,0]

# OP_codes
# 1 = add
# 2 = multiply
# 99 = halt

STEP_SIZE = 4

def process_instruction(index, program):
    """ Process the instruction at the given index

        index = pointer to code word
        index+0 = op_code (1= add, 2=multiply, 99=halt)
        index+1 = address of argument1
        index+2 = address of argument2
        index+3 = address of result

    """

    halt_program = False

    op_code = program[index]

    if op_code == 99:
        halt_program = True

    elif op_code in [1,2]:

        arg1 = program[program[index+1]]
        arg2 = program[program[index+2]]
        result_address = program[index+3]

        if op_code == 1:
            program[result_address] = arg1 + arg2
        elif op_code == 2:
            program[result_address] = arg1 * arg2

    elif op_code == 99:
        halt_program = True

    else:
        print('Unknown op_code. Halting operation.')
        halt_program = True

    return halt_program

def run_program(program):
    """ Run the given program """
    halt = False
    prog_index = 0

    while not halt:
        halt = process_instruction(prog_index, program)
        prog_index += STEP_SIZE

    return program

def main():
    """ Main program """

    assert run_program(TEST_1) == TEST_1_RESULT
    assert run_program(TEST_2) == TEST_2_RESULT
    assert run_program(TEST_3) == TEST_3_RESULT
    assert run_program(TEST_4) == TEST_4_RESULT

    print("Tests passed")

    print("Running 1202 program...")
    PROGRAM[1] = 12
    PROGRAM[2] = 2
    run_program(PROGRAM)
    print(PROGRAM[0])

if __name__ == "__main__":
    main()

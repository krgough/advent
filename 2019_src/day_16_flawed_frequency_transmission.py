'''
Created on 16 Dec 2019

@author: Keith.Gough

Advent of Code 2019 - Day 16: Flawed Frequency Transmission


Could not solve part 2 without a lot of help from the reddit channel.

'''
import math

TEST_1_INT = 12345678
TEST_2_INT = 80871224585914546619083218645595
TEST_3_INT = 19617804207202209144916044189917
TEST_4_INT = 69317163492948606335995924319873

TEST_1 = [int(dig) for dig in list(str(TEST_1_INT))]
TEST_2 = [int(dig) for dig in list(str(TEST_2_INT))]
TEST_3 = [int(dig) for dig in list(str(TEST_3_INT))]
TEST_4 = [int(dig) for dig in list(str(TEST_4_INT))]

TEST_2_RES = 24176176
TEST_3_RES = 73745418

BASE_PATTERN = [0, 1, 0, -1]




def load_data(filename):
    """ Load puzzle data """
    with open(filename, 'r') as file:
        my_data = str(file.read())

    my_data = [int(dig) for dig in list(my_data)]
    return my_data

def find_base_value(index, element):
    return BASE_PATTERN[((index + 1) // (element + 1)) % 4]
def yield_base_value(element, start, stop):
    """ Iterator for base value for given element index """
    for i in range(start, stop):
        yield find_base_value(i, element)
def last_digit(num):
    """ Returns absolute value of last digit of an integer """
    return abs(num) % 10

def create_pattern(element, len_required):
    """ Create pattern multiplier """
    base_pattern = [0, 1, 0, -1]
 
    element_base = [i for i in base_pattern for _ in range(element + 1)]
    #print(element_base)
 
    number_required = (math.ceil(len_required / len(element_base))) + 1
    element_pattern = (element_base * number_required)[1:len_required + 1]
    return element_pattern

def fft_part1(data, phases):
    """ Calculate a single phase of the fft

        Multiply each digit in data by it's corresponding digit in element_pattern
        Take the abs last digit of the calculation and store it as the output

    """
    for _ in range(phases):
        result = []
        for ele in range(len(data)):
            element_pattern = create_pattern(ele, len(data))
            res = 0
            #for j, _ in enumerate(data):
            for i, val in enumerate(data):
                #res = data[i] * element_pattern[i]
                res += data[i] * find_base_value(i, ele)

                #print(element_pattern[i], find_base_value(i, ele))
                #assert res1 == res

            result.append(last_digit(res))
        data = result
    return data


def fft_part2(data, message_index, phases):
    """ Calculate a single phase of the fft

        If we are looking for a message in the FFR at a position in the
        second half then we can ignore the first half of the input as
        it does not contribute the the 2nd half output.

        We also note that the 2nd half of the calculation is the reverse
        partial sum of the input.

    """
    data = data[message_index:]

    for _ in range(phases):
        psum = 0
        for i in range(len(data)-1, -1, -1):
            psum += data[i]
            data[i] = last_digit(psum)
    return data

def main():
    """ Main Program """

    data = TEST_3
    data = fft_part1(data, 100)
    res = int(''.join([str(d) for d in data[0:8]]))
    assert res == TEST_3_RES

    print('Part 1:')
    data = load_data('day_16_data.txt')
    data = fft_part1(data, 100)
    res = int(''.join([str(d) for d in data[0:8]]))
    print(res)

    print('\nPart 2:')
    data = load_data('day_16_data.txt') * 10000
    message_offset = int(''.join([str(d) for d in data[0:7]]))
    result = fft_part2(data, message_offset, 100)
    res = int(''.join([str(r) for r in result[:8]]))
    print(res)

if __name__ == "__main__":
    main()

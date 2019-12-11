'''
Created on 8 Dec 2019

@author: Keith.Gough

Advent of Code 2019 - Day 8: Space Image Format

'''

import re

TEST_1 = '123456689012'
TEST_2 = '0222112222120000'

TEST_1_LAYER_SIZE = 3 * 2
TEST_2_LAYER_SIZE = 2 * 2

LAYER_SIZE = 25 * 6

PIX_CLEAR = 2
PIX_BLACK = 0
PIX_WHITE = 1

def load_file(filename):
    """ load data file """
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append(line.strip())
    return data

def first_visible_pixel(pixel_data):
    """ Find the visible pixel """
    for pix in pixel_data:
        if pix in ['0', '1']:
            return pix
    return None
def process_layers_old(raw_image, img_size):
    """ test """

    pixel_data = []

    for i in range(0, img_size):
        pixel_data.append(raw_image[i::150])

    v_pix = []
    for pix in pixel_data:
        pix_list = list(pix)
        print(pix_list)
        v_pix.append(first_visible_pixel(pix_list))

    print()
    print(v_pix)

    return v_pix
def process_layers(raw_image, img_size):
    """ Create a list of strings where each string contains the layer value for that pixel

        Create a list of strings where each string contains the layer value for that pixel
        str1 = pixel1 = [l1, l2, l3 ...]
        ...

    """
    pixel_data = [raw_image[i::img_size] for i in range(img_size)]

    vis_pix = ''
    for pix_index in range(img_size):
        pix = re.search('[01]', pixel_data[pix_index]).span()[0]
        vis_pix += pixel_data[pix_index][pix]

    return vis_pix
def print_image(image, row_size):
    """ Print out the image """
    img = ''.join(image)
    img = img.replace("0", ' ')

    for i in range(0, len(img), row_size):
        print(img[i:i+row_size])
def layer_checksum(raw_img):
    """ Find the layer in the img with min number of zeros
        Calculate the number of 1s * number of 2s on that layer.

    """
    char_counts = {}
    for i in range(0, len(raw_img), LAYER_SIZE):
        layer = raw_img[i:i + LAYER_SIZE]
        char_counts[layer.count('0')] = [layer.count('1'), layer.count('2')]

    min_zeros = min(char_counts)
    checksum = char_counts[min_zeros][0] * char_counts[min_zeros][1]
    print("Part1: Layer with minimum zeros\n")
    print(f"Minimum zeros = {min_zeros} zeros.")
    print(f"Ones*Twos     = {checksum}")
    return checksum

def main():
    """ Main Program """
    raw_img = load_file('day_08_data.txt')[0]

    # Part 1
    layer_checksum(raw_img)

    # Part 2
    layer_size = LAYER_SIZE
    row_size = 25
    print("\nPart2: Password Image\n")
    img = process_layers(raw_img, layer_size)
    print_image(img, row_size)

if __name__ == "__main__":
    main()

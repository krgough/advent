'''
Created on 2 Dec 2019

@author: Keith.Gough
'''

import math

FILENAME = 'day_1_data.txt'

def load_data(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append(int(line.strip()))
    return data

def fuel_required(module_mass):
    """ Calculate the fuel required to launch the module 

        Fuel required to launch a given module is based on its mass.
        Specifically, to find the fuel required for a module, take its mass,
        divide by three, round down, and subtract 2.
    """
    return math.floor(module_mass/3) - 2

def main():
    """ Main Program """
    module_mass_data = load_data(FILENAME)

    # Run test vectors
    assert fuel_required(12) == 2
    assert fuel_required(14) == 2
    assert fuel_required(1969) == 654
    assert fuel_required(100756) == 33583
    print ('Tests pass')

    # Calculate answer
    total_fuel = 0
    for module_mass in module_mass_data:
        total_fuel += fuel_required(module_mass)
    print(total_fuel)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
'''
Created on 2 Dec 2019

@author: Keith.Gough

Advent of Code 2019 - Day 1 Task

'''

import math

FILENAME = 'day_1_data.txt'

def load_data(filename):
    """ Load the mass data file """
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append(int(line.strip()))
    return data

def simple_fuel_required(module_mass):
    """ Calculate the fuel required to launch the module

        Fuel required to launch a given module is based on its mass.
        Specifically, to find the fuel required for a module, take its mass,
        divide by three, round down, and subtract 2.
    """
    fuel_mass = max(0, math.floor(module_mass/3) - 2)

    return fuel_mass

# def total_fuel_required(module_mass):
#     """ Use a loop here and keep calling till we get zero """
#     fuel_mass = simple_fuel_required(module_mass)
#
#     extra = fuel_mass
#     while extra > 0:
#         extra = simple_fuel_required(extra)
#         fuel_mass += extra
#
#     return fuel_mass

def total_fuel_required(module_mass):
    """ Use recursion to calculate total fuel required """
    fuel = simple_fuel_required(module_mass)
    if fuel <= 0:
        return fuel
    return fuel + total_fuel_required(fuel)

def main():
    """ Main Program """
    module_mass_data = load_data(FILENAME)

    # Run test vectors
    assert simple_fuel_required(12) == 2
    assert simple_fuel_required(14) == 2
    assert simple_fuel_required(1969) == 654
    assert simple_fuel_required(100756) == 33583

    assert total_fuel_required(1969) == 966
    print('Tests pass')

    # Calculate part1 answer
    simple_fuel = []
    for module_mass in module_mass_data:
        simple_fuel.append(simple_fuel_required(module_mass))

    print(f'Simple Fuel Total (Part 1) = {sum(simple_fuel)}')

    # Calculate part2 answer
    complex_fuel = []
    for module_mass in module_mass_data:
        complex_fuel.append(total_fuel_required(module_mass))
    print(f"Total fuel required (Part 2) = {sum(complex_fuel)}")


if __name__ == "__main__":
    main()

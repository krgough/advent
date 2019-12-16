'''
Created on 14 Dec 2019

@author: Keith.Gough


Advent of Code 2019 - Day 14: Space Stoichiometry

'''
from math import ceil


TEST_1 = """
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
"""

def load_file(filename):
    """ Load the data """
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file]

    recipes = {}
    counts = {'ORE': 0}
    for line in lines:
        line = line.split(" => ")
        # list of tuples for the inputs to a reaction (qty, name)
        comps = [(int(y[0]), y[1]) for y in [x.strip().split(' ') for x in line[0].split(',')]]
        # list of tuples for the outputs to a reaction (qty, name)
        prods = [(int(y[0]), y[1]) for y in [x.strip().split(' ') for x in line[1].split(',')]]
        #print(comps, prods)

        # Stash the recipe in a dict with key = product name
        recipes[prods[0][1]] = (comps, prods)

        # Counts of produced ingredients
        counts[prods[0][1]] = 0

    return recipes, counts

def make_product(qty, prod, recipes, counts):
    """ Make qantity = qty of what

        Recurse back through the list until we get to ORE
        Keep a running count of inngredient quantities made
        For each required ingedient:
            If insufficient already made then make the required amount.

        Stop recursing when we reach ORE

        At the end the counts['ORE'] will be negative and show the
        ORE requirement.

    """

    # We don't make ORE so stop the recursion here
    if prod == 'ORE':
        return

    print(f"Recipe = {recipes[prod]}")

    # What product are we short of
    missing = qty - counts[prod]
    print(f"Missing {missing} units of {prod}")

    # Work out how many iterations of the recipe we need to run
    if missing > 0:
        runs = ceil(missing/recipes[prod][1][0][0])
    else:
        return

    # Now make each of the ingredients
    # Do this n times as required to make the qty of the product
    for ingredient in recipes[prod][0]:
        ing_qty = ingredient[0] * runs
        print(f"To make {qty} {prod} we need {ing_qty} {ingredient[1]}.")
        # Produce that ingredient and consume some of ingredients
        make_product(ingredient[0] * runs,
                     ingredient[1],
                    recipes,
                    counts)
        counts[ingredient[1]] -= ingredient[0] * runs

    # After making the product increase our count of that product
    counts[prod] += recipes[prod][1][0][0] * runs

def calculate_ore_for_x_fuel(fuel_qty):
    """ Calculate ORE required for x batches of fuel """
    recipes, counts = load_file('day_14.txt')
    make_product(fuel_qty, 'FUEL', recipes, counts)
    print(counts)
    return -counts['ORE']

def main():
    """ Main Program """

    # Part 1
    ore = calculate_ore_for_x_fuel(1)
    print(f"Part 1:  Ore for one unit of fuel = {ore}")

    ore = calculate_ore_for_x_fuel(4200533)
    if ore > 1000000000000:
        print('SMALLER')
    else:
        print("LARGER")

if __name__ == "__main__":
    main()
                 
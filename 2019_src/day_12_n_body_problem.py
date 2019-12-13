'''
Created on 12 Dec 2019

@author: Keith.Gough

Advent of Code 2019 - Day 12: N Body Problem

Calculate velocities based on gravit by coparing moon pairs and increasing x, y, z
velocity component on each moon by +/-1 in order to pull the moons closer together.

Calculate new position for each moon by applying the velocities to the moons position.

'''

import itertools
import functools
import logging
from copy import deepcopy

LOGGER = logging.getLogger(__name__)

MOON_COMBINATIONS = list(itertools.combinations(range(4),2))

POSITIONS = [
    {'x':  6, 'y': 10, 'z': 10},
    {'x': -9, 'y':  3, 'z': 17},
    {'x':  9, 'y': -4, 'z': 14},
    {'x':  4, 'y': 14, 'z':  4},
    ]

VELOCITIES =[
    {'x': 0, 'y': 0, 'z': 0},
    {'x': 0, 'y': 0, 'z': 0},
    {'x': 0, 'y': 0, 'z': 0},
    {'x': 0, 'y': 0, 'z': 0},
    ]

TEST_1_POS = [
    {'x': -1, 'y':   0, 'z':  2},
    {'x':  2, 'y': -10, 'z': -7},
    {'x':  4, 'y':  -8, 'z':  8},
    {'x':  3, 'y':   5, 'z': -1},
    ]

TEST_1_POS_10TH_ITER = [
    {'x': 2, 'y':  1, 'z': -3},
    {'x': 1, 'y': -8, 'z':  0},
    {'x': 3, 'y': -6, 'z':  1},
    {'x': 2, 'y':  0, 'z':  4},
    ]

TEST_1_VEL_10TH_ITER = [
    {'x': -3, 'y': -2, 'z':  1},
    {'x': -1, 'y':  1, 'z':  3},
    {'x':  3, 'y':  2, 'z': -3},
    {'x':  1, 'y': -1, 'z': -1},
    ]

TEST_2_POS = [
    {'x': -8, 'y': -10, 'z':  0},
    {'x':  5, 'y':   5, 'z': 10},
    {'x':  2, 'y':  -7, 'z':  3},
    {'x':  9, 'y':  -8, 'z': -3},
]


def update_velocities(positions, velocities):
    """ Apply gravity to calculate new velocities for the moons

        For each combination of moons apply gravity to each velocity
        component.  Adjust  the velocity component by +/-1 to move
        the moons together.  If position component is equal then
        add zero to the velocity component.
    """
    for comb in MOON_COMBINATIONS:
        moon1_vel = velocities[comb[0]]
        moon1_pos = positions[comb[0]]

        moon2_vel = velocities[comb[1]]
        moon2_pos = positions[comb[1]]

        for comp in ['x', 'y', 'z']:
            if moon1_pos[comp] == moon2_pos[comp]:
                delta = 0
            elif moon1_pos[comp] > moon2_pos[comp]:
                delta = -1
            else:
                delta = 1

            moon1_vel[comp] = moon1_vel[comp] + delta
            moon2_vel[comp] = moon2_vel[comp] - delta

def update_positions(positions, velocities):
    """ Add velocity components to each moons position components
    """
    for moon in range(4):
        for comp in ['x', 'y', 'z']:
            positions[moon][comp] = positions[moon][comp] + velocities[moon][comp]

def update_moons(positions, velocities, iterations):
    """ Make one iteration of moon positions and velocities
    """
    for _ in range(1, iterations+1):
        update_velocities(positions, velocities)
        update_positions(positions, velocities)

def matches_start_state(positions,velocities, wrk_posn, wrk_vels, comp):
    """ Find when the component returns to initial value """
    for moon in range(4):
        if (positions[moon][comp] != wrk_posn[moon][comp] or
            velocities[moon][comp] != wrk_vels[moon][comp]):
            return False
    return True

def find_cycles(positions, velocities):
    """ Find the earliest time when all planets return to their initial
        position and velocity.

        Note that X, Y, Z are idependant, so we can look for cycles in the components
        of each planet and find the lowest common multiple of them all i.e.

        Find step for fist return to start for 3 groups...

        P0x,v, P1x,y, P2x,v and P3x,v
        P0y,v, P1y,y, P2y,v and P3y,v
        P0z,v, P1z,y, P2z,v and P3z,v

        Then find least common multiple of those values.

    """
    cycles = []

    for comp in ['x', 'y' , 'z']:
        wrk_posn = deepcopy(positions)
        wrk_vels = deepcopy(velocities)

        cycle_found = False
        iteration = 0

        while not cycle_found:

            iteration += 1
            update_moons(wrk_posn, wrk_vels, 1)

            if matches_start_state(positions, velocities, wrk_posn, wrk_vels, comp):
                print(iteration)
                cycle_found = True
                cycles.append(iteration)

    return cycles

def calculate_total_energy(positions, velocities):
    """ Total energy = potential + kinetic

        potential energy = sum of the absolute values of its x, y, and z position components.
        kinetic energy   = sum of the absolute values of its velocity components.
    """
    total_energy = 0

    for moon in range(4):
        potential_e = sum([abs(positions[moon][comp]) for comp in positions[moon]])
        kinetic_e = sum([abs(velocities[moon][comp]) for comp in velocities[moon]])
        total_energy += (potential_e * kinetic_e)

    return total_energy

def gcd(a,b):
    """ Greatest common divisor """
    while b:
        a,b = b, a%b
    return a

def lcm(a,b):
    """ Lowest common multiple """
    return a*b // gcd(a,b)


#LCM = functools.reduce(lambda x, y: lcm(x, y), [2,22000000001])

def main():
    """ Main Program """

    positions = deepcopy(TEST_1_POS)
    velocities = deepcopy(VELOCITIES)
    update_moons(positions, velocities, 10)
    assert positions == TEST_1_POS_10TH_ITER
    assert velocities == TEST_1_VEL_10TH_ITER
    total_energy = calculate_total_energy(positions, velocities)
    assert total_energy == 179
    print(f"Part 1: Total energy = {total_energy}")

    print("\nPart 2:")
    positions = deepcopy(POSITIONS)
    velocities = deepcopy(VELOCITIES)
    cycles = find_cycles(positions, velocities)

    # Finds the lowest common multiple from a list of values
    lcm_cycles = functools.reduce(lcm, cycles)
    print(f"All objectes return to initial state at step : {lcm_cycles})")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()

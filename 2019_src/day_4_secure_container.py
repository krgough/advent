'''
Created on 4 Dec 2019

@author: Keith.Gough

Advent of Code 2019 - Day4 Task

'''
from collections import Counter

def check_pin(pin):
    """ Return True if:

        Length of pin == 6
        and
        Digits are increasing from right to left (or are equal)
        and
        At least one repeating digit
    """
    # We number the digits from the right starting with index=0
    # Check than 1>=0, 2>=1... n>=n-1

    # Zip 2 lists into a list of tuples [(d1,d2). (d2, d3] ....]
    # Then check the tuple 2nd position is always larger or equal than 1st posn
    # Check that at least one tuple has identical values
    # Check the list length is 6

    pin_list = [int(digit) for digit in str(pin)]
    zipped = list(zip(pin_list, pin_list[1:]))

    non_decreasing = all([i[0] <= i[1] for i in zipped])
    repeat_digit = any([i[0] == i[1] for i in zipped])

    return non_decreasing & repeat_digit & (len(pin_list) == 6)

def find_pin_candidates(from_pin, to_pin):
    """ Find pin candidates from the given range """
    candidates = []
    for pin in range(from_pin, to_pin+1):
        if check_pin(pin):
            candidates.append(pin)
    return candidates

def exclude_repeats(candidates):
    """ Find candidates that have at least one digit that only
        repeats twice in the pin.

        Since we know the candidates are ordered we know that any repeating
        digit is already adjacent to its other instances.  So if we simply
        count occurences and confirm that we have only one digit that has
        an occurence of 2, then that is a valid candidate.
    """
    reduced_candidate_list = []
    for candidate in candidates:

        cand_str = str(candidate)
        digit_count = Counter(cand_str)

        # Check we have at least one digit that has a count of 2
        if 2 in digit_count.values():
            reduced_candidate_list.append(candidate)

    return reduced_candidate_list

def exclude_repeats_old(candidates):
    """ Find candidates that have at least one digit that only
        repeats twice in the pin.

        Since we know the candidates are ordered we know that any repeating
        digit is already adjacent to its other instances.  So if we simply
        count occurences and confirm that we have only one digit that has
        an occurence of 2, then that is a valid candidate.
    """
    reduced_candidate_list = []
    for candidate in candidates:
        cand_str = str(candidate)
        digit_count = {}
        for digit in cand_str:
            digit_count[digit] = cand_str.count(digit)

        # Check we have at least one digit that has a count of 2
        if 2 in digit_count.values():
            reduced_candidate_list.append(candidate)
    return reduced_candidate_list

def main():
    """ Main Program """
    # Tests
    assert not check_pin(223450)
    assert check_pin(111111)
    assert not check_pin(123789)

    # Part 1
    # Run 1st part search for pin candidates
    candidates = find_pin_candidates(387638, 919123)
    print(f"Part 1: Number of candidates = {len(candidates)}")

    # Part 2
    # Find candidates that have at least one digit that only repeats twice
    candidates = exclude_repeats(candidates)
    print(f"Part 2: Number of candidates with single repeats = {len(candidates)}")

if __name__ == "__main__":
    main()

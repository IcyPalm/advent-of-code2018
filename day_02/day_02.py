import os
from collections import Counter
from itertools import combinations

with open(os.path.join(os.path.dirname(__file__), 'input')) as input_file:
    data = input_file.read().splitlines()


def part1():
    threes = 0
    twos = 0
    for line in data:
        linecount = Counter(line)
        if 2 in linecount.values():
            twos += 1
        if 3 in linecount.values():
            threes += 1
    return threes*twos


def part2():
    for first, second in combinations(data, 2):
        compare = [i for i, j in zip(first, second) if i == j]
        if len(first) - len(compare) == 1:
            return "".join(compare)


if __name__ == "__main__":
    print(f'Part one: {part1()}')
    print(f'Part two: {part2()}')

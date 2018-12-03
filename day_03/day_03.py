import os
import re
from itertools import product

with open(os.path.join(os.path.dirname(__file__), 'input')) as input_file:
    data = input_file.read().splitlines()


def part1():
    field = {}
    for line in data:
        chunks = re.findall(r"[\w]+", line)
        left = int(chunks[1])
        top = int(chunks[2])
        size = chunks[3].split('x')
        size_x = int(size[0])
        size_y = int(size[1])
        for x, y in product(range(left, left+size_x),  range(top, top+size_y)):
            if (x, y) not in field.keys():
                field[(x, y)] = 1
            else:
                field[(x, y)] += 1
    return sum(i > 1 for i in field.values())


def part2():
    answer = "Part two answer"
    return answer


if __name__ == "__main__":
    print(f'Part one: {part1()}')
    print(f'Part two: {part2()}')

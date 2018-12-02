import os

with open(os.path.join(os.path.dirname(__file__), 'input')) as input_file:
    data = input_file.read().rstrip()


def part1():
    answer = "Part one answer"
    return answer


def part2():
    answer = "Part two answer"
    return answer


if __name__ == "__main__":
    print(f'Part one: {part1()}')
    print(f'Part two: {part2()}')

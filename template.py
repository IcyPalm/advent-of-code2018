import os

with open(os.path.join(os.path.dirname(__file__), 'input')) as input_file:
    data = input_file.read().rstrip()


def part1():
    return data


def part2():
    return data


if __name__ == "__main__":
    # TODO: Save output to file or pass output so can be automatically submitted
    print(part1())
    print(part2())

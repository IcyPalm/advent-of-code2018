import os

with open(os.path.join(os.path.dirname(__file__), 'input')) as input_file:
    data = input_file.readlines()


def part1():
    frequency = 0
    for time_shift in data:
        frequency += int(time_shift)
    answer = frequency
    return answer


def part2():
    frequency_list = {0}
    current_frequency = 0
    while True:
        for time_shift in data:
            current_frequency += int(time_shift)
            if current_frequency in frequency_list:
                return current_frequency
            frequency_list.add(current_frequency)


if __name__ == "__main__":
    print(f'Part one: {part1()}')
    print(f'Part two: {part2()}')

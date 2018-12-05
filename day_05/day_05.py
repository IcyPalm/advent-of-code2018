import os

with open(os.path.join(os.path.dirname(__file__), 'input')) as input_file:
    data = input_file.read().rstrip()


def part1():
    contains_units = True
    new_string = data
    while contains_units:
        current_letter, next_letter = "", ""
        x = 0
        temp_string = ""
        contains_units = False
        while x < len(new_string)-1:
            current_letter = new_string[x]
            next_letter = new_string[x+1]
            if current_letter.isupper() and next_letter.islower() and current_letter.lower()==next_letter:
                x += 1
                contains_units = True
            elif current_letter.islower() and next_letter.isupper() and current_letter.upper()==next_letter:
                x += 1
                contains_units = True
            else:
                temp_string += current_letter
            x += 1
        new_string = temp_string + next_letter
    return len(new_string)


def part2():
    answer = "Part two answer"
    return answer


if __name__ == "__main__":
    print(f'Part one: {part1()}')
    print(f'Part two: {part2()}')

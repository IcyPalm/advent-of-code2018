import os
from datetime import datetime

with open(os.path.join(os.path.dirname(__file__), 'input')) as input_file:
    data = input_file.read().splitlines()


def part1():
    eventlist = {}
    for moment in data:
        event_time = datetime.strptime(moment[1:17], '%Y-%m-%d %H:%M')
        event = moment[19:]
        eventlist[event_time] = event

    guardlist = {}
    current_guard = 0
    fall_asleep = 0
    for key in sorted(eventlist.keys()):
        if 'Guard' in eventlist[key]:
            current_guard = int(eventlist[key].split()[1].strip('#'))
            if current_guard not in guardlist.keys():
                guardlist[current_guard] = dict.fromkeys(list(range(0, 60)), 0)
        elif 'falls' in eventlist[key]:
            fall_asleep = int(datetime.strftime(key, '%M'))
        else:
            wake_up = int(datetime.strftime(key, '%M'))
            for minute in range(fall_asleep, wake_up):
                guardlist[current_guard][minute] += 1
    summed_guardlist = {}
    for guard, minutelist in guardlist.items():
        summed_guardlist[guard] = sum(minutelist.values())
    sleepiest_guard = max(summed_guardlist, key=summed_guardlist.get)
    sleepiest_minute = max(guardlist[sleepiest_guard], key=guardlist[sleepiest_guard].get)

    return sleepiest_guard*sleepiest_minute


def part2():
    answer = "Part two answer"
    return answer


if __name__ == "__main__":
    print(f'Part one: {part1()}')
    print(f'Part two: {part2()}')

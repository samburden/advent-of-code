import heapq
import time

def part1():
    calories = readCalories()

    print('Part 1:', max(calories))


def part2():
    calories = readCalories()
    calories.sort(reverse=True)

    print('Part 2:', sum(calories[:3]))

def readCalories():
    calories = []

    with open('inputs/input1.txt') as f:
        curCals = 0
        for line in f:
            if line.strip():
                curCals += int(line)
            else:
                calories.append(curCals)
                curCals = 0

    return calories

if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)
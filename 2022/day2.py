import time

def part1():
    combos = {'A X': 4, 'A Y': 8, 'A Z': 3, 'B X': 1, 'B Y': 5, 'B Z': 9, 'C X': 7, 'C Y': 2, 'C Z': 6}
    print('Part 1:', findSolution(combos))


def part2():
    combos = {'A X': 3, 'A Y': 4, 'A Z': 8, 'B X': 1, 'B Y': 5, 'B Z': 9, 'C X': 2, 'C Y': 6, 'C Z': 7}
    print('Part 2:', findSolution(combos))

def findSolution(combos):
    total = 0

    with open('inputs/input2.txt') as f:
        for line in f:
            total += combos[line.strip()]

    return total

if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)
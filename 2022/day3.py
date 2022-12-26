import time

def part1():
    print('Part 1:', findSolution())

def part2():
    print('Part 2:', findSolution(True))

def findSolution(isPart2=False):
    items = []

    with open('inputs/input3.txt') as f:
        if isPart2:
            for line1, line2, line3 in zip(f, f, f):
                items.append(list(set(line1.strip()) & set(line2.strip()) & set(line3.strip()))[0])
        else:
            for line in f:
                mid = len(line) // 2
                items.append(list(set(line[:mid]) & set(line[mid:]))[0])

    total = 0
    for i in items:
        if i.isupper():
            total += ord(i) - ord('A') + 27
        else:
            total += ord(i) - ord('a') + 1

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
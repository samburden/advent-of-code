import time
def part1():
    print('Part 1:', findOverlaps())


def part2():
    print('Part 2:', findOverlaps(True))

def findOverlaps(isPart2=False):
    ans = 0

    with open('inputs/input4.txt') as f:
        for line in f:
            elf1, elf2 = line.split(',')
            s1, e1 = map(int, elf1.split('-'))
            s2, e2 = map(int, elf2.split('-'))

            if isPart2 and s1 <= e2 and e1 >= s2:
                ans += 1
            elif (s1 <= s2 and e1 >= e2) or (s2 <= s1 and e2 >= e1):
                ans += 1

    return ans


if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)
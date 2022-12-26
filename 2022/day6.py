from collections import defaultdict
import time

def part1():
    print('Part 1:', findStart(readData(), 4))

def part2():
    print('Part 2:', findStart(readData(), 14))

def readData():
    with open('inputs/input6.txt') as f:
        return f.readline()

def findStart(buffer, n):
    cur = defaultdict(int)
    l, r = 0, 0
    while len(cur.keys()) < n:
        cur[buffer[r]] += 1

        if r - l > n - 1:
            cur[buffer[l]] -= 1
            if cur[buffer[l]] == 0:
                del cur[buffer[l]]
            l += 1
        r += 1

    return r

if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)
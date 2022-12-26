import time

def part1():
    print('Part 1:', runSimulation())

def part2():
    print('Part 2:', runSimulation(True))

def runSimulation(isPart2=False):
    ans = ""
    stacks = [[] for _ in range(9)]
    pos = [1, 5, 9, 13, 17, 21, 25, 29, 33]
    with open('inputs/input5.txt') as f:
        for line in f:
            if len(line.strip()) > 25:
                if line[1] == "1":
                    continue

                for i, p in enumerate(pos):
                    if p < len(line) and line[p] != " ":
                        stacks[i] = [line[p]] + stacks[i]
            elif line.strip():
                action = line.strip().split()
                cnt, fromStack, toStack = int(action[1]), int(action[3]) - 1, int(action[5]) - 1
                stackToMove = []
                for _ in range(cnt):
                    if isPart2:
                        stackToMove = [stacks[fromStack].pop()] + stackToMove
                    else:
                        stacks[toStack].append(stacks[fromStack].pop())

                stacks[toStack].extend(stackToMove)

    for s in stacks:
        ans += s[-1]

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
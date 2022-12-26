import time
import math
from collections import Counter

def part1():
    elves = getElves()
    print('Part 1:', runSimulation1(elves, 10))
def part2():
    elves = getElves()
    print('Part 2:', runSimulation2(elves, 1000))

def getElves():
    elves = []
    with open('inputs/input23.txt') as f:
        i = 0
        for line in f:
            line = line.strip()
            if line:
                for j, c in enumerate(line):
                    if c == '#':
                        elves.append((i, j))
            i += 1

    return elves

def runSimulation1(elves, rounds):
    elfSet = set(elves)
    movements = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    directions = [[[-1, -1], [-1, 0], [-1, 1]],
                  [[1, -1], [1, 0], [1, 1]],
                  [[-1, -1], [0, -1], [1, -1]],
                  [[-1, 1], [0, 1], [1, 1]]]
    allDirections = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

    for r in range(rounds):
        curDir = r % 4
        # Get proposals
        proposals = []
        for r, c in elves:
            foundElfAround = False
            for dr, dc in allDirections:
                pr, pc = r + dr, c + dc
                if (pr, pc) in elfSet:
                    foundElfAround = True
                    break
            if not foundElfAround:
                proposals.append((r, c))
                continue

            nDir = curDir
            foundNewDir = False
            for i in range(4):
                valid = True
                for dr, dc in directions[nDir]:
                    pr, pc = r + dr, c + dc
                    if (pr, pc) in elfSet:
                        valid = False
                        break
                if not valid:
                    nDir = (nDir + 1) % 4
                else:
                    mr, mc = movements[nDir]
                    proposals.append((r + mr, c + mc))
                    foundNewDir = True
                    break
            if not foundNewDir:
                proposals.append((r, c))

        # Check proposals
        proposalSet = Counter(proposals)
        newElves = []
        for i, coords in enumerate(proposals):
            r, c = coords
            if proposalSet[(r, c)] > 1:
                newElves.append(elves[i])
            else:
                newElves.append((r, c))

        elves = newElves
        elfSet = set(elves)

    minR, maxR, minC, maxC = findMaxes(elves)

    return findEmptySpots(elfSet, minR, maxR, minC, maxC)

def runSimulation2(elves, rounds):
    elfSet = set(elves)
    movements = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    directions = [[[-1, -1], [-1, 0], [-1, 1]],
                  [[1, -1], [1, 0], [1, 1]],
                  [[-1, -1], [0, -1], [1, -1]],
                  [[-1, 1], [0, 1], [1, 1]]]
    allDirections = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

    for rnd in range(rounds):
        curDir = rnd % 4
        # Get proposals
        proposals = []
        for r, c in elves:
            foundElfAround = False
            for dr, dc in allDirections:
                pr, pc = r + dr, c + dc
                if (pr, pc) in elfSet:
                    foundElfAround = True
                    break
            if not foundElfAround:
                proposals.append((r, c))
                continue

            nDir = curDir
            foundNewDir = False
            for i in range(4):
                valid = True
                for dr, dc in directions[nDir]:
                    pr, pc = r + dr, c + dc
                    if (pr, pc) in elfSet:
                        valid = False
                        break
                if not valid:
                    nDir = (nDir + 1) % 4
                else:
                    mr, mc = movements[nDir]
                    proposals.append((r + mr, c + mc))
                    foundNewDir = True
                    break
            if not foundNewDir:
                proposals.append((r, c))

        # Check proposals
        proposalSet = Counter(proposals)
        newElves = []
        for i, coords in enumerate(proposals):
            r, c = coords
            if proposalSet[(r, c)] > 1:
                newElves.append(elves[i])
            else:
                newElves.append((r, c))

        if not (elfSet - set(newElves)):
            return rnd + 1

        elves = newElves
        elfSet = set(elves)


def findMaxes(elves):
    minR = math.inf
    maxR = -math.inf
    minC = math.inf
    maxC = -math.inf

    for r, c in elves:
        minR = min(minR, r)
        maxR = max(maxR, r)
        minC = min(minC, c)
        maxC = max(maxC, c)

    return minR, maxR, minC, maxC

def findEmptySpots(elfSet, minR, maxR, minC, maxC):
    emptySpots = 0
    for r in range(minR, maxR + 1):
        for c in range(minC, maxC + 1):
            if (r, c) not in elfSet:
                emptySpots += 1

    return emptySpots

if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)
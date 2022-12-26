import time
import re
import math
from functools import lru_cache

def part1():
    blueprints = readBlueprints()

    total = 0
    for b in blueprints:
        val = runSimulation(b, 24)
        total += b[0] * val

    print('Part 1:', total)


def part2():
    blueprints = readBlueprints()

    total = 1
    for b in blueprints[:3]:
        val = runSimulation(b, 32)
        total *= val

    print('Part 2:', total)

def readBlueprints():
    blueprints = []
    with open('inputs/input19.txt') as f:
        for line in f:
            line = line.strip()
            if line:
                b = list(map(int, re.findall(r'\d+', line)))
                blueprints.append(b)

    return blueprints
def runSimulation(blueprint, startTime):
    blueprintId, oreCost, clayCost, obOreCost, obClayCost, geoOreCost, geoObCost = blueprint
    costs = [[oreCost], [clayCost], [obOreCost, obClayCost], [geoOreCost, 0, geoObCost]]
    maxCosts = [max(oreCost, clayCost, obOreCost, geoOreCost), obClayCost, geoObCost, math.inf]

    # State first contains the counts of materials: ore, clay, obsidian, geode
    # Next state contains the counts of robots: ore, clay, obsidian, geode
    curState = ((0, 0, 0, 0), (1, 0, 0, 0))
    visited = {}
    @lru_cache(None)
    def dfs(state, timeLeft):
        if timeLeft <= 0:
            return 0

        # Check if worse state
        if (timeLeft, state[1]) in visited and not any([a > b for a, b in zip(state[0], visited[(timeLeft, state[1])])]):
            return 0

        visited[(timeLeft, state[1])] = state[0]

        # Collect materials
        newMaterialCnts = [min(m + r, timeLeft * mx) for m, r, mx in zip(state[0], state[1], maxCosts)]
        best = newMaterialCnts[3]

        # Attempt to build a robot
        curMaterials = list(state[0])
        for i, c in enumerate(costs):
            curRobots = list(state[1])
            # Check if enough material and if we don't already have enough robots
            haveMaterials = all([curMaterials[i] >= c[i] for i in range(len(c))])
            if haveMaterials and curRobots[i] < maxCosts[i]:
                remainingMaterials = [newMaterialCnts[i] - (c[i] if i < len(c) else 0)
                                      for i in range(len(newMaterialCnts))]
                #print(remainingMaterials)
                curRobots[i] += 1
                best = max(best, dfs((tuple(remainingMaterials), tuple(curRobots)), timeLeft - 1))

        # No robot built
        best = max(best, dfs((tuple(newMaterialCnts), state[1]), timeLeft - 1))

        return best

    return dfs(curState, startTime)

if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)
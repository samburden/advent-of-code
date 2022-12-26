import time
import math
import sys
sys.setrecursionlimit(10000)

def part1():
    coords = readCoords()

    print('Part 1:', getSurfaceArea(coords))


def part2():
    coords = readCoords()

    # First find all cubes of the droplet including air pockets
    coords = findAllCubesInDroplet(coords)

    # Now run same algorithm from part 1
    print('Part 1:', getSurfaceArea(coords))

def readCoords():
    coords = []
    with open('inputs/input18.txt') as f:
        for line in f:
            line = line.strip()
            if line:
                coords.append(tuple(map(int, line.split(','))))

    return coords
def getSurfaceArea(coords):
    coordSet = set(coords)

    # Direction to check: right, left, top, bottom, back, front
    directions = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
    total = 0
    for x, y, z in coords:
        for dx, dy, dz in directions:
            nx, ny, nz = x + dx, y + dy, z + dz
            if (nx, ny, nz) not in coordSet:
                total += 1

    return total

# This returns all the cubes in the droplet including air
def findAllCubesInDroplet(coords):
    minMaxX, minMaxY, minMaxZ = getMinMax(coords)
    dropletSet = set(coords)
    allCoords = []

    outsideAir = set()

    # Direction to move for DFS: right, left, top, bottom, back, front
    directions = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]

    # Run DFS to find all the outsize air start from top left
    def dfs(x, y, z):
        outsideAir.add((x, y, z))
        for dx, dy, dz in directions:
            nx, ny, nz = x + dx, y + dy, z + dz
            if (nx, ny, nz) not in dropletSet and (nx, ny, nz) not in outsideAir \
                and minMaxX[0] - 1 <= nx <= minMaxX[1] + 1 and minMaxY[0] - 1 <= ny <= minMaxY[1] + 1 \
                    and minMaxZ[0] - 1 <= nz <= minMaxZ[1] + 1:
                dfs(nx, ny, nz)

    dfs(minMaxX[0] - 1, minMaxY[0] - 1, minMaxZ[0] - 1)

    # Now go through every cube and see if it's part of droplet or outside air
    for x in range(minMaxX[0], minMaxX[1] + 1):
        for y in range(minMaxY[0] - 1, minMaxY[1] + 1):
            for z in range(minMaxZ[0] - 1, minMaxZ[1] + 1):
                if (x, y, z) in dropletSet:
                    allCoords.append((x, y, z))
                elif (x, y, z) not in outsideAir:
                    allCoords.append((x, y, z))

    print('# of air pockets: ', len(allCoords) - len(dropletSet))
    return allCoords

# This could be better implemented with something like numpy
def getMinMax(coords):
    minX, maxX = math.inf, -math.inf
    minY, maxY = math.inf, -math.inf
    minZ, maxZ = math.inf, -math.inf

    for x, y, z in coords:
        minX = min(minX, x)
        maxX = max(maxX, x)
        minY = min(minY, y)
        maxY = max(maxY, y)
        minZ = min(minZ, z)
        maxZ = max(maxZ, z)

    return (minX, maxX), (minY, maxY), (minZ, maxZ)

if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)
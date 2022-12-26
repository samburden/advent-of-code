import time

def part1():
    grid = buildGrid(readPoints(), 200, 600)

    print('Part 1:', runSimulation(grid, 0, 500))

def part2():
    # cheated a little here by finding the max depth and then just harding maxDepth + 2.
    # Also made the grid arbitrarily wide to contain all the sand. This isn't the best solution.
    grid = buildGrid(readPoints(), 164, 1000)

    for j in range(len(grid[0])):
        grid[-1][j] = '#'

    print('Part 2:', runSimulation(grid, 0, 500))

def readPoints():
    data = []
    with open('inputs/input14.txt') as f:
        for line in f:
            line = line.strip()
            data.append(line.split('->'))

    return data

def buildGrid(data, r, c):
    grid = [['.'] * c for _ in range(r)]
    for points in data:
        for i in range(1, len(points)):
            c1, r1 = [int(c.strip()) for c in points[i-1].split(',')]
            c2, r2 = [int(c.strip()) for c in points[i].split(',')]
            if r1 == r2:
                c1, c2 = min(c1, c2), max(c1,c2)
                for j in range(c1, c2+1):
                    grid[r1][j] = '#'
            else:
                r1, r2 = min(r1, r2), max(r1, r2)
                for j in range(r1, r2 + 1):
                    grid[j][c1] = '#'

    return grid

def runSimulation(grid, r, c, maxDepth=199):

    sandCnt = 0
    while True:
        cameToRest = False
        curR, curC = r, c
        while not cameToRest:
            if curR >= maxDepth:
                return sandCnt
            if grid[curR+1][curC] == '.':
                curR += 1
            elif grid[curR+1][curC-1] == '.':
                curR += 1
                curC -= 1
            elif grid[curR+1][curC+1] == '.':
                curR += 1
                curC += 1
            else:
                grid[curR][curC] = 'o'
                sandCnt += 1
                cameToRest = True
                if curR == r and curC == c:
                    return sandCnt



if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)
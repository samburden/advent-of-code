import numpy as np
import time

def part1():

    grid = readGrid()

    R, C = len(grid), len(grid[0])
    treeSet = set()
    # View from top
    columnFirst(grid, treeSet, R, C)

    # View from bottom
    columnFirst(grid, treeSet, R, C, True)

    # View from left
    rowFirst(grid, treeSet, R, C)

    # View from right
    rowFirst(grid, treeSet, R, C, True)

    print('Part 1:', len(treeSet))

def part2():
    grid = readGrid()
    grid = np.array(grid)

    R, C = len(grid), len(grid[0])
    scenicGrid = np.empty((R, C, 4), int)

    # Build views from right and left
    for i in range(R):
        scenicGrid[i, :, 0] = buildStack(grid[i, :])
        scenicGrid[i, :, 1] = buildStack(grid[i, :][::-1])[::-1]
    # Build views from bottom and top
    for j in range(C):
        scenicGrid[:, j, 2] = buildStack(grid[:, j])
        scenicGrid[:, j, 3] = buildStack(grid[:, j][::-1])[::-1]

    ans = 0
    for i in range(R):
        for r, l, b, t in scenicGrid[i]:
            ans = max(ans, r*l*b*t)


    print('Part 2:', ans)

def readGrid():
    grid = []
    with open('inputs/input8.txt') as f:
        for line in f:
            grid.append(list(map(int, list(line.strip()))))

    return grid

def columnFirst(grid, treeSet, R, C, reverse=False):
    rows = range(R) if not reverse else range(R - 1, -1, -1)
    for j in range(C):
        maxTree = -1
        for i in rows:
            if grid[i][j] > maxTree:
                maxTree = grid[i][j]
                if (i,j) not in treeSet:
                    treeSet.add((i,j))

def rowFirst(grid, treeSet, R, C, reverse=False):
    columns = range(C) if not reverse else range(C - 1, -1, -1)

    for i in range(R):
        maxTree = -1
        for j in columns:
            if grid[i][j] > maxTree:
                maxTree = grid[i][j]
                if (i,j) not in treeSet:
                    treeSet.add((i,j))

# Use monotonic stack
def buildStack(heights):
    ans = [len(heights) - i - 1 for i in range(len(heights))]
    stack = []

    for i, h in enumerate(heights):
        while stack and h >= stack[-1][0]:
            sh, si = stack.pop()
            ans[si] = abs(i - si)
        stack.append((h,i))

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

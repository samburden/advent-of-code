from collections import deque
import time

def part1():
    grid, s, e = buildGrid()

    print('Part 1:', bfs(grid, [s], e))



def part2():
    grid, s, e = buildGrid()

    sourceNodes = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 'a':
                sourceNodes.append((r,c))

    print('Part 2:', bfs(grid, sourceNodes, e))

def buildGrid():
    grid = []
    s = e = None
    with open('inputs/input12.txt') as f:
        for line in f:
            line = line.strip()
            if not s:
                potentialS = line.find('S')
                if potentialS > -1:
                    s = (len(grid), potentialS)
                    line = line[:potentialS] + 'a' + line[potentialS + 1:]
            if not e:
                potentialE = line.find('E')
                if potentialE > -1:
                    e = (len(grid), potentialE)
                    line = line[:potentialE] + 'z' + line[potentialE + 1:]

            grid.append(list(line))

    return grid, s, e

def bfs(grid, s, e):
    R, C = len(grid), len(grid[0])
    q = deque(s)
    steps = 0
    directions = [[1,0], [-1,0], [0,1], [0,-1]]
    visited = set()
    visited.update(s)

    while q:
        n = len(q)
        for _ in range(n):
            r, c = q.popleft()
            if (r, c) == e:
                return steps

            height = ord(grid[r][c])

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                if min(nr, nc) >= 0 and nr < R and nc < C and (nr,nc) not in visited and ord(grid[nr][nc]) <= height + 1:
                    q.append((nr, nc))
                    visited.add((nr, nc))

        steps += 1

    return -1


if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)
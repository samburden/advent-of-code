import time
import math
from collections import deque, defaultdict

def part1():
    grid, blizzards = buildGrid()
    print('Part 1:', runSimulation(grid, blizzards, [(len(grid) - 1, len(grid[0]) - 2)]))
def part2():
    grid, blizzards = buildGrid()
    ends = [(len(grid) - 1, len(grid[0]) - 2), (0,1), (len(grid) - 1, len(grid[0]) - 2)]
    print('Part 2:', runSimulation(grid, blizzards, ends))

def buildGrid():
    grid = []
    blizzards = defaultdict(list)
    with open('inputs/input24.txt') as f:
        i = 0
        directions = {'^': 0, '>': 1, 'v': 2, '<': 3}
        for line in f:
            line = line.strip()
            if line:
                grid.append(list(line))
                for j, c in enumerate(line):
                    if c in {'>', '<', '^', 'v'}:
                        blizzards[(i-1, j-1)].append(directions[c])
            i += 1

    return grid, blizzards

def runSimulation(grid, blizzards, ends):
    R, C = len(grid) - 2, len(grid[0]) - 2
    directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    q = deque()
    q.append((0,1))
    time = 0
    curEnd = 0

    while True:
        # Move blizzards first
        newBlizzards = defaultdict(list)
        for r, c in blizzards:
            for b in blizzards[(r,c)]:
                nr, nc = r + directions[b][0], c + directions[b][1]
                nr, nc = nr % R, nc % C
                newBlizzards[(nr,nc)].append(b)
        blizzards = newBlizzards

        # Now try to move elves:
        n = len(q)
        visited = set()
        for _ in range(n):
            r, c = q.popleft()
            # check if end found and move to next end if it exists. Reset the queue to current end
            if ends[curEnd] == (r,c):
                if curEnd + 1 >= len(ends):
                    return time
                curEnd += 1
                q = deque()
                q.append((r,c))
                print(time)
                break
            # Try to move each direction
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if nr >= 0 and nr < len(grid) and grid[nr][nc] != '#' and (nr-1, nc-1) not in blizzards and (nr,nc) not in visited:
                    q.append((nr, nc))
                    visited.add((nr, nc))
            # Other option is to stay in place if no blizzard is at current position
            if (r-1, c-1) not in blizzards and (r,c) not in visited:
                q.append((r,c))
                visited.add((r,c))

        time += 1

if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)
import time
import math
import numpy as np

def part1():
    grid, instructions, rows, cols = buildGrid(16)

    r, c, curDir = runSimulation(grid, instructions, rows, cols)
    print(r, c, curDir)
    print('Part 1:', r * 1000 + c * 4 + curDir)
def part2():
    grid, instructions, rows, cols = buildGrid(150)
    # For test file
    #facesCoords = [[0,4,8,12], [4,8,0,4], [4,8,4,8], [4,8,8,12], [8,12,8,12], [8,12,12,16]]
    facesCoords = [[0, 50, 50, 100], [0, 50, 100, 150],
                   [50, 100, 50, 100], [100, 150, 0, 50],
                   [100, 150, 50, 100], [150, 200, 0, 50]]
    faces = buildFaces(np.array(grid), facesCoords)
    # For test file
    # movements = [[[5, -1, 2], [3, 1, 1], [2, 1, 1], [1, -1, 1]],
    #               [[2, 1, 0], [4, 1, 3], [5, -1, 3], [0, -1, 2]],
    #               [[3, 1, 0], [4, -1, 0], [1, 1, 2], [0, 1, 0]],
    #               [[5, -1, 1], [4, 1, 1], [2, 1, 3], [0, 1, 3]],
    #               [[5, 1, 0], [1, -1, 3], [2, -1, 3], [3, 1, 3]],
    #               [[0, -1, 2], [1, -1, 0], [4, 1, 2], [3, -1, 2]]]

    movements = [[[1, 1, 0], [2, 1, 1], [3, -1, 0], [5, 1, 0]],
                 [[4, -1, 2], [2, 1, 2], [0, 1, 2], [5, 1, 3]],
                 [[1, 1, 3], [4, 1, 1], [3, 1, 1], [0, 1, 3]],
                 [[4, 1, 0], [5, 1, 1], [0, -1, 0], [2, 1, 0]],
                 [[1, -1, 2], [5, 1, 2], [3, 1, 2], [2, 1, 3]],
                 [[4, 1, 3], [1, 1, 1], [0, 1, 1], [3, 1, 3]]]

    f, r, c, curDir = runSimulation2(faces, instructions, movements, 50)
    print(f, r, c, curDir)
    r, c = facesCoords[f][0] + r, facesCoords[f][2] + c
    print(r, c, curDir)
    print('Part 2:', r * 1000 + c * 4 + curDir)

def buildGrid(maxLen):
    grid = []
    rows = {}
    cols = {}
    intstructionTxt = ''
    with open('inputs/input22.txt') as f:
        i = 0
        for line in f:
            if line.strip():
                if line[0].isdigit():
                    intstructionTxt = line.strip()
                else:
                    line = line.rstrip()
                    # This is ugly and needs to be improved with regex or another method
                    l, r = min(line.find('#') if not line.find('#') == -1 else math.inf,
                               line.find('.') if not line.find('.') == -1 else math.inf), len(line) - 1
                    rows[i] = [l, r]
                    for j in range(len(line)):
                        if line[j] != ' ':
                            if j in cols:
                                cols[j] = [min(cols[j][0], i), max(cols[j][1], i)]
                            else:
                                cols[j] = [i, i]
                    grid.append(list(line.ljust(maxLen, ' ')))
                    i += 1
    instructions = []
    curNum = ''
    for c in intstructionTxt:
        if c in {'R','L'}:
            instructions.append(curNum)
            instructions.append(c)
            curNum = ''
        else:
            curNum += c
    if len(curNum):
        instructions.append(curNum)

    return grid, instructions, rows, cols

def buildFaces(grid, faceCoords):
    faces = []
    for rMin, rMax, cMin, cMax in faceCoords:
        faces.append(grid[rMin:rMax, cMin:cMax])

    return faces

def runSimulation(grid, instructions, rows, cols):
    directions = [[0,1], [1,0], [0,-1], [-1,0]]
    curDir = 0
    r, c = 0, rows[0][0]

    for ins in instructions:
        if ins in {'R', 'L'}:
            curDir = (curDir + 1 if ins == 'R' else curDir - 1) % 4
        else:
            steps = int(ins)
            for i in range(steps):
                nr, nc = r + directions[curDir][0], c + directions[curDir][1]
                if curDir == 0 and nc > rows[nr][1]:
                    nc = rows[nr][0]
                elif curDir == 1 and nr > cols[nc][1]:
                    nr = cols[nc][0]
                elif curDir == 2 and nc < rows[nr][0]:
                    nc = rows[nr][1]
                elif curDir == 3 and nr < cols[nc][0]:
                    nr = cols[nc][1]

                if grid[nr][nc] == '#':
                    break

                r, c = nr, nc

    return r + 1, c + 1, curDir

def runSimulation2(faces, instructions, movements, size):
    directions = [[0,1], [1,0], [0,-1], [-1,0]]
    curDir = 0
    f, r, c = 0, 0, 0

    for ins in instructions:
        if ins in {'R', 'L'}:
            curDir = (curDir + 1 if ins == 'R' else curDir - 1) % 4
        else:
            steps = int(ins)
            for i in range(steps):
                nr, nc = r + directions[curDir][0], c + directions[curDir][1]
                nDir = curDir
                nFace = f
                if (curDir == 0 and nc >= size) or \
                        (curDir == 1 and nr >= size) or \
                        (curDir == 2 and nc < 0) or \
                        (curDir == 3 and nr < 0):
                    nFace, rev, nDir = movements[f][curDir]
                    nr, nc = getNewCoords(r, c, nr, nc, nDir, curDir, rev, size)

                if faces[nFace][nr][nc] == '#':
                    break

                r, c, f, curDir = nr, nc, nFace, nDir

    return f, r + 1, c + 1, curDir

# This is really ugly and needs to be done a different way
def getNewCoords(r, c, nr, nc, nDir, curDir, rev, size):
    if nDir == curDir and (nDir == 0 or nDir == 2):
        nc = 0 if nDir == 0 else size - 1
    elif nDir == curDir and (nDir == 1 or nDir == 3):
        nr = 0 if nDir == 1 else size - 1
    elif nDir == 0:
        nc = 0
        if curDir == 1 or curDir == 3:
            nr = c if rev == 1 else (size - 1) - c
        elif curDir == 2:
            nr = r if rev == 1 else (size - 1) - r
    elif nDir == 1:
        nr = 0
        if curDir == 0 or curDir == 2:
            nc = r if rev == 1 else (size - 1) - r
        elif curDir == 3:
            nc = c if rev == 1 else (size - 1) - c
    elif nDir == 2:
        nc = size - 1
        if curDir == 0:
            nr = r if rev == 1 else (size - 1) - r
        elif curDir == 1 or curDir == 3:
            nr = c if rev == 1 else (size - 1) - c
    elif nDir == 3:
        nr = size - 1
        if curDir == 0 or curDir == 2:
            nc = r if rev == 1 else (size - 1) - r
        elif curDir == 1:
            nc = c if rev == 1 else (size - 1) - c


    return nr, nc


if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)
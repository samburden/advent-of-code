import time

class Shape:
    def __init__(self, coords):
        self.coords = coords

    def moveLeft(self):
        newCoords = []
        for x, y in self.coords:
            newCoords.append([x, y + 1])
        return newCoords

    def moveRight(self):
        newCoords = []
        for x, y in self.coords:
            newCoords.append([x, y - 1])
        return newCoords

    def moveDown(self):
        newCoords = []
        for x, y in self.coords:
            newCoords.append([x - 1, y])
        return newCoords
class ShapeFactory:
    def createShape(self, shape, bottom):
        if shape == 'cross':
            return Shape([[bottom, 3], [bottom + 1, 4], [bottom + 1, 3], [bottom + 1, 2], [bottom + 2, 3]])
        elif shape == 'LShape':
            return Shape([[bottom, 4], [bottom, 3], [bottom, 2], [bottom + 1, 2], [bottom + 2, 2]])
        elif shape == 'HLine':
            return Shape([[bottom, 4], [bottom, 3], [bottom, 2], [bottom, 1]])
        elif shape == 'VLine':
            return Shape([[bottom, 4], [bottom + 1, 4], [bottom + 2, 4], [bottom + 3, 4]])
        else:
            return Shape([[bottom, 4], [bottom + 1, 4], [bottom, 3], [bottom + 1, 3]])

def part1():
    movements = readMovements()

    print('Part 1:', runSimulation(movements, 2022)[0])


def part2():
    movements = readMovements()

    curTop, heights = runSimulation(movements, 50000)
    start, windowLen, windowSum = findRepeatingWindow(heights)
    print(f"Window start: {start}, Window length: {windowLen}, Window sum: {windowSum}")

    priorToStart = heights[start]
    q, remainder = divmod(1000000000000 - start, windowLen)
    middleCnt = q * windowSum
    remainder = heights[start + remainder - 1] - heights[start]
    print(int(priorToStart + middleCnt + remainder))

def readMovements():
    with open('inputs/input17.txt') as f:
        movements = f.readline().strip()

    return movements
def runSimulation(movements, rocks):
    shapes = ['HLine', 'cross', 'LShape', 'VLine', 'square']
    linesToAdd = [4, 6, 6, 7, 5]
    grid = []
    m, n = len(movements), len(shapes)
    imov, ishape = 0, 0
    cnt = 0
    curTop = -1
    shapeFactory = ShapeFactory()
    heights = []

    while cnt < rocks:
        grid.extend([['.'] * 7 for _ in range(max(0, linesToAdd[ishape] - (len(grid) - curTop - 1)))])
        shape = shapeFactory.createShape(shapes[ishape], curTop + 4)

        # begin movement
        while True:
            # Attempt to move left or right
            if movements[imov] == '<':
                newCoords = shape.moveLeft()
            else:
                newCoords = shape.moveRight()

            imov = (imov + 1) % m

            # Check if valid
            if checkIfValid(grid, newCoords):
                shape.coords = newCoords

            # Attempt to move down
            newCoords = shape.moveDown()

            # Check if valid
            if checkIfValid(grid, newCoords):
                shape.coords = newCoords
            else:
                stopRock(grid, shape.coords)
                ishape = (ishape + 1) % n
                cnt += 1
                curTop = max(curTop, shape.coords[-1][0])
                break
        heights.append(curTop + 1)

    return curTop + 1, heights
def checkIfValid(grid, newCoords):
    for x, y in newCoords:
        if not 0 <= y < len(grid[0]) or not x >= 0 or grid[x][y] != '.':
            return False

    return True


def stopRock(grid, newCoords):
    for x, y in newCoords:
        grid[x][y] = '#'

def findRepeatingWindow(heights):
    maxLength = len(heights) // 2
    for windowLen in range(2, maxLength):
        for i in range(len(heights) - windowLen):
            windowSum = heights[i + windowLen] - heights[i]
            nextWinStart = i + windowLen
            nextWinStop = nextWinStart + windowLen
            repeats = 0
            while max(nextWinStart, nextWinStop) < len(heights) and windowSum == (heights[nextWinStop] - heights[nextWinStart]):
                repeats += 1
                if repeats > 5:
                    return i, windowLen, windowSum
                nextWinStart, nextWinStop = nextWinStart + windowLen, nextWinStop + windowLen

if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)
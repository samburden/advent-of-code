import time

def part1():
    importantCycles = {20, 60, 100, 140, 180, 220}
    cycle, x = 0, 1
    ans = []
    operations = readOperations()

    for op in operations:
        if op == 'noop':
            cycle += 1
            checkImportant(cycle, x, ans, importantCycles)
        else:
            cycle += 1
            checkImportant(cycle, x, ans, importantCycles)
            cycle += 1
            checkImportant(cycle, x, ans, importantCycles)
            x += int(op.split()[1])

    print('Part 1:', sum(ans))


def part2():
    cycle, x = 0, 1
    curSprite = {0,1,2}
    ans = [['.'] * 40 for _ in range(6)]
    drawPixel(cycle, curSprite, ans)
    operations = readOperations()

    for op in operations:
        if op == 'noop':
            cycle += 1
            drawPixel(cycle, curSprite, ans)
        else:
            cycle += 1
            drawPixel(cycle, curSprite, ans)
            cycle += 1
            drawPixel(cycle, curSprite, ans)
            x += int(op.split()[1])
            curSprite = {x - 1, x, x + 1}

    print('Part 2:')
    for r in ["".join(row) for row in ans]:
        print(r)

def readOperations():
    operations = []

    with open('inputs/input10.txt') as f:
        for line in f:
            operations.append(line.strip())

    return operations

def checkImportant(cycle, x, ans, importantCycles):
    if cycle in importantCycles:
        ans.append(x * cycle)

def drawPixel(cycle, curSprite, ans):
    if (cycle - 1) % 40 in curSprite:
        r, c = (cycle - 1) // 40, (cycle - 1) % 40
        ans[r][c] = '#'

if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)
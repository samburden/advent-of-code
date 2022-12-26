import time

def part1():
    head = tail = (50, 50)
    visited = set()
    visited.add(tail)
    movements = readMovements()

    for dir, cnt in movements:
        cnt = int(cnt)
        for _ in range(cnt):
            prevHead = head
            if dir == 'L':
                head = (head[0], head[1] - 1)
            elif dir == 'R':
                head = (head[0], head[1] + 1)
            elif dir == 'U':
                head = (head[0] - 1, head[1])
            else:
                head = (head[0] + 1, head[1])

            # Check if head more than 1 away from tail
            if max(abs(head[0] - tail[0]), abs(head[1] - tail[1])) > 1:
                tail = (tail[0] + (prevHead[0] - tail[0]), tail[1] + (prevHead[1] - tail[1]))
                visited.add(tail)
    print('Part 1:', len(visited))


def part2():
    rope = [(50, 50)] * 10
    visited = set()
    visited.add((50, 50))
    movements = readMovements()

    for dir, cnt in movements:
        cnt = int(cnt)
        for c in range(cnt):
            if dir == 'L':
                rope[0] = (rope[0][0], rope[0][1] - 1)
            elif dir == 'R':
                rope[0] = (rope[0][0], rope[0][1] + 1)
            elif dir == 'U':
                rope[0] = (rope[0][0] - 1, rope[0][1])
            else:
                rope[0] = (rope[0][0] + 1, rope[0][1])

            for i in range(1, len(rope)):
                # Check if prev knot more than 1 away from current knot
                if max(abs(rope[i-1][0] - rope[i][0]), abs(rope[i-1][1] - rope[i][1])) > 1:
                    dx = dy = 0
                    if rope[i-1][0] != rope[i][0] and rope[i-1][1] != rope[i][1]:
                        dx = -1 if rope[i-1][0] < rope[i][0] else 1
                        dy = -1 if rope[i-1][1] < rope[i][1] else 1
                    elif rope[i-1][0] != rope[i][0]:
                        dx = -1 if rope[i - 1][0] < rope[i][0] else 1
                    else:
                        dy = -1 if rope[i - 1][1] < rope[i][1] else 1
                    rope[i] = (rope[i][0] + dx, rope[i][1] + dy)
                    if i == len(rope) - 1:
                        visited.add(rope[i])
                else:
                    break

    print('Part 2:', len(visited))

def readMovements():
    movements = []

    with open('inputs/input9.txt') as f:
        for line in f:
            movements.append(line.strip().split())

    return movements

if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)
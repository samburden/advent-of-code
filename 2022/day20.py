import time

def part1():
    nums = readFile()

    nums = runSimulation(nums, 1, 1)
    n = len(nums)
    # Find 0
    i = nums.index(0)

    # Find 1000th after 0
    n1 = nums[(i + 1000) % n]

    # Find 2000th after 0
    n2 = nums[(i + 2000) % n]

    # Find 3000th after 0
    n3 = nums[(i + 3000) % n]

    print(n1, n2, n3)
    print('Part 1:', n1 + n2 + n3)



def part2():
    nums = readFile()

    nums = runSimulation(nums, 10, 811589153)
    n = len(nums)
    # Find 0
    i = nums.index(0)

    # Find 1000th after 0
    n1 = nums[(i + 1000) % n]

    # Find 2000th after 0
    n2 = nums[(i + 2000) % n]

    # Find 3000th after 0
    n3 = nums[(i + 3000) % n]

    print(n1, n2, n3)
    print('Part 2:', n1 + n2 + n3)

def readFile():
    nums = []
    with open('inputs/input20.txt') as f:
        for line in f:
            line = line.strip()
            if line:
                nums.append(int(line))

    return nums
def runSimulation(nums, rounds, decryptionKey):
    n = len(nums)
    nums = [nums[i] * decryptionKey for i in range(n)]
    indexes = [i for i in range(n)]

    for _ in range(rounds):
        for i in range(n):
            curIndex = indexes.index(i)
            newPos = (curIndex + nums[i]) % (n - 1)
            if newPos == 0:
                indexes.append(indexes.pop(curIndex))
            else:
                indexes.insert(newPos, indexes.pop(curIndex))

    return [nums[i] for i in indexes]

if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)
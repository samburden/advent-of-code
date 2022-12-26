import time

def part1():
    sensors, beacons = readFile()

    print('Part 1:', determineCoverage(sensors, beacons, 2000000))


# Completely brute force.
# I'm sure there is some math/geometry that I'm not familiar with that could solve this quicker
# Takes about 90s to run
def part2BF():
    sensors, beacons = readFile()

    maxY = 4000000
    found = False
    for y in range(maxY):
        x = 0
        while x <= maxY:
            for s, b in zip(sensors, beacons):
                potentialNewX = skipX(s, b, x, y)
                if x != potentialNewX:
                    break

            if potentialNewX == x:
                print(f"{x}:{y}")
                print('Part 2:', x * maxY + y)
                found = True
                break

            x = potentialNewX
        if found:
            break

# Slight optimization over brute force that uses intervals
# This runs in about 35s
def part2():
    sensors, beacons = readFile()
    distances = [getDistance(s, b) for s,b in zip(sensors, beacons)]

    maxY = 4000000
    for y in range(maxY):
        intervals = []
        for s, d in zip(sensors, distances):
            interval = getRange(s, d, y)
            if interval:
                interval = [max(0, interval[0]), min(maxY, interval[1])]
                intervals.append(interval)


        mergedIntervals = mergeIntervals(intervals)
        if len(mergedIntervals) > 1:
            # Found two intervals, now determine if there is a gap
            # If there is a gap we found our coordinates
            if mergedIntervals[1][0] - mergedIntervals[0][1] >= 2:
                print(f"{mergedIntervals[0][1] + 1}:{y}")
                print('Part 2:', (mergedIntervals[0][1] + 1) * 4000000 + y)
                break

def readFile():
    sensors = []
    beacons = []
    with open('inputs/input15.txt') as f:
        for line in f:
            s, b = processLine(line.strip())
            sensors.append(s)
            beacons.append(b)

    return sensors, beacons

def processLine(line):
    # This is ugly and would be better with regx
    sensorTxt, beaconTxt = line.split(':')
    sensorXTxt, sensorYTxt = sensorTxt.split(',')
    sensorX = int(sensorXTxt.split('=')[1])
    sensorY = int(sensorYTxt.split('=')[1])
    beaconXTxt, beaconYTxt = beaconTxt.split(',')
    beaconX = int(beaconXTxt.split('=')[1])
    beaconY = int(beaconYTxt.split('=')[1])

    return (sensorX, sensorY), (beaconX, beaconY)

def determineCoverage(sensors, beacons, concernedY):
    covered = set()
    senAndBea = set(sensors)
    senAndBea.update(set(beacons))

    for s, b in zip(sensors, beacons):
        distance = abs(s[0] - b[0]) + abs(s[1] - b[1])
        curDistance = abs(s[1] - concernedY)
        if distance - curDistance < 0:
            continue

        curX = s[0]
        covered.add(curX)

        i = 1
        curDistance += 1
        while curDistance <= distance:
            if (curX + i, concernedY) not in senAndBea: covered.add(curX + i)
            if (curX - i, concernedY) not in senAndBea: covered.add(curX - i)
            curDistance += 1
            i += 1


    return len(covered)

def skipX(s, b, x, y):
    distance = abs(s[0] - b[0]) + abs(s[1] - b[1])

    diff = distance - abs(s[1] - y)

    if diff > 0 and s[0] - diff <= x < s[0] + diff:
        return s[0] + diff + 1

    return x

def getDistance(s, b):
    return abs(s[0] - b[0]) + abs(s[1] - b[1])

def getRange(s, d, y):

    diff = d - abs(s[1] - y)

    if diff >= 0:
        return (s[0] - diff, s[0] + diff)

    return None

# Taken from https://www.geeksforgeeks.org/merging-intervals/
def mergeIntervals(intervals):
    # Sort the array on the basis of start values of intervals.
    intervals.sort()
    stack = []
    # insert first interval into stack
    stack.append(intervals[0])
    for i in intervals[1:]:
        # Check for overlapping interval,
        # if interval overlap
        if stack[-1][0] <= i[0] <= stack[-1][1]:
            stack[-1][1] = max(stack[-1][1], i[1])
        else:
            stack.append(i)

    return stack

if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)
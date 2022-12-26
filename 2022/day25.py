import time

def part1():
    data = readData()
    nums = convertData(data)
    s = sum(nums)
    print('Sum:', s)
    print('Part 1:', convertToSnafu(s))

def readData():
    data = []
    with open('inputs/input25.txt') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(line)

    return data

def convertData(data):
    nums = []
    conversion = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
    for snafu in data:
        p = 0
        num = 0
        for c in snafu[::-1]:
            num += conversion[c] * (5**p)
            p += 1
        nums.append(num)

    return nums

def convertToSnafu(num, prevPow=-1):
    if prevPow == 0:
        return ''
    p = findSignificantPower(abs(num))
    digit = '0' * (prevPow - p - 1) if prevPow > -1 else ''
    if num > 0:
        if num >= 5**(p) + (5**(p) / 2):
            digit += '2'
            rem = num - (5**p * 2)
        else:
            digit += '1'
            rem = num - 5**p
    elif num < 0:
        if num <= (5**p * -1) - (5**(p) / 2):
            digit += '='
            rem = num - (5**p * -2)
        else:
            digit += '-'
            rem = num - (5**p * -1)
    else:
        return '0'

    return digit + convertToSnafu(rem, p)

def findSignificantPower(num):
    p = 0
    while num > (5**(p+1) / 2):
        p += 1

    return p

if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
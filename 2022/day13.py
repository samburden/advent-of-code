from ast import literal_eval
from functools import cmp_to_key
from math import prod
import time

def part1():
    packets = readPackets()
    i, pair = 1, 1
    ans = []
    while i < len(packets):
        if compare(packets[i-1], packets[i]) <= 0:
            ans.append(pair)
        i += 2
        pair += 1

    print('Part 1:', sum(ans))

def part2():
    packets = readPackets()

    packets.extend([[[2]], [[6]]])
    packets.sort(key=cmp_to_key(compare))

    print('Part 2:', prod([i + 1 for i, p in enumerate(packets) if compare(p, [[2]]) == 0 or compare(p, [[6]]) == 0]))

def readPackets():
    packets = []
    with open('inputs/input13.txt') as f:
        for line in f:
            line = line.strip()
            if line:
                packets.append(literal_eval(line))

    return packets
def compare(packet1, packet2):
    res = 0
    for i in range(min(len(packet1), len(packet2))):
        if isinstance(packet1[i], int) and isinstance(packet2[i], int):
            res = (packet1[i] > packet2[i]) - (packet1[i] < packet2[i])
        elif isinstance(packet1[i], list) and isinstance(packet2[i], list):
            res = compare(packet1[i], packet2[i])
        elif isinstance(packet1[i], list) and isinstance(packet2[i], int):
            res = compare(packet1[i], [packet2[i]])
        elif isinstance(packet1[i], int) and isinstance(packet2[i], list):
            res = compare([packet1[i]], packet2[i])

        if res:
            return res

    return (len(packet1) > len(packet2)) - (len(packet1) < len(packet2))

if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)
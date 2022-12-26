import time
from collections import deque
from functools import lru_cache


class Valve:
    def __init__(self, name, rate, tunnels=[]):
        self.name = name
        self.rate = rate
        self.tunnels = tunnels

    def __str__(self):
        return f"Name: {self.name}, Rate: {self.rate}, Tunnels: {','.join(self.tunnels)}"

def part1():
    graph = readGraph()

    print('Part 1:', findSolution(graph, 'AA', 30))

def part2():
    graph = readGraph()

    print('Part 2:', findSolution2(graph, 'AA', 26))

def readGraph():
    graph = {}
    with open('inputs/input16.txt') as f:
        for line in f:
            line = line.strip()
            if line:
                name, valve = processLine(line)
                graph[name] = valve

    return graph

def processLine(line):
    # This is ugly and would be better with regx
    valveTxt, tunnelsTxt = line.split(';')
    rate = int(valveTxt.split('=')[1])
    valveName = valveTxt[6:8]
    if 'tunnels' in tunnelsTxt:
        tunnelsTxt = tunnelsTxt.strip()[23:]
    else:
        tunnelsTxt = tunnelsTxt.strip()[22:]
    tunnels = list(map(str.strip, tunnelsTxt.split(',')))

    return valveName, Valve(valveName, rate, tunnels)

def findSolution(graph, start, time):

    @lru_cache(None)
    def dfs(v, timeLeft, op, cntToOpen):
        if timeLeft <= 0 or cntToOpen <= 0:
            return 0

        # Turn tuple into set
        opened = {i for i in op}

        pressure = 0
        # First option open a valve
        if v not in opened and graph[v].rate > 0:
            newOpened = {v} | opened
            pressure = max(pressure, (graph[v].rate * (timeLeft - 1)) +
                           dfs(v, timeLeft - 1, tuple(newOpened), cntToOpen - 1))

        # Go down tunnels
        for c in graph[v].tunnels:
            pressure = max(pressure, dfs(c, timeLeft - 1, op, cntToOpen))

        return pressure

    return dfs(start, time, (), len([graph[k].rate for k in graph if graph[k].rate > 0]))

# This is really slow. Original code didn't include the score optimization and took more than 30m to run.
# I found the idea for the score optimization to short circuit the recursion on Reddit https://www.reddit.com/r/adventofcode/comments/zn6k1l/2022_day_16_solutions/
# Now it runs in about 1m
def findSolution2(graph, start, time):
    visited = {}

    @lru_cache(None)
    def dfs(v, e, timeLeft, op, cntToOpen, score):
        if timeLeft <= 0 or cntToOpen <= 0:
            return 0

        # Turn tuple into set
        opened = {i for i in op}

        if visited.get((v, e, timeLeft), -1) >= score:
           return 0
        visited[(v, e, timeLeft)] = score

        pressure = 0
        curScore = score + sum([graph[k].rate for k in graph if k in opened])
        # I open a valve
        if v not in opened and graph[v].rate > 0:
            myPressure = (graph[v].rate * (timeLeft - 1))

            # Elephant also opens their valve
            if v != e and e not in opened and graph[e].rate > 0:
                ourPressure = myPressure + (graph[e].rate * (timeLeft - 1))
                newOpened = {v} | {e} | opened
                newScore = curScore + graph[v].rate + graph[e].rate
                pressure = max(pressure, ourPressure +
                               dfs(v, e, timeLeft - 1, tuple(newOpened), cntToOpen - 2, newScore))

            # Elephant goes somewhere
            for ce in graph[e].tunnels:
                newOpened = {v} | opened
                newScore = curScore + graph[v].rate
                pressure = max(pressure, myPressure + dfs(v, ce, timeLeft - 1, tuple(newOpened), cntToOpen - 1, newScore))

        # I go down a tunnel
        for c in graph[v].tunnels:

            # Elephant open it's valve
            if e not in opened and graph[e].rate > 0:
                elephantPressure = (graph[e].rate * (timeLeft - 1))
                newOpened = {e} | opened
                newScore = curScore + graph[e].rate
                pressure = max(pressure,  elephantPressure +
                               dfs(c, e, timeLeft - 1, tuple(newOpened), cntToOpen - 1, newScore))

            # Elephant walks as well
            for ce in graph[e].tunnels:
                pressure = max(pressure, dfs(c, ce, timeLeft - 1, op, cntToOpen, curScore))

        return pressure

    return dfs(start, start, time, (), len([graph[k].rate for k in graph if graph[k].rate > 0]), 0)

# This was done after getting hints from Reddit https://www.reddit.com/r/adventofcode/comments/zn6k1l/2022_day_16_solutions/
def findSolutionOptimized(graph, start, time):
    keyValves = {v for v in graph if graph[v].rate > 0 or v == start}
    distances = findAllDistances(graph, keyValves)


    def dfs(v, timeLeft, visited=set(), targetValves=keyValves):
        visited = visited | {v}
        targetValves = targetValves - visited
        pressure = 0
        # Go down tunnels
        for kv in targetValves:
            myTimeLeft = timeLeft - distances[(v, kv)] - 1
            if myTimeLeft > 0:
                pressure = max(pressure, graph[kv].rate * myTimeLeft + dfs(kv, myTimeLeft, visited, targetValves))

        return pressure

    return dfs(start, time)

def findAllDistances(graph, keyValves):
    distances = {}

    for v in graph:
        if v not in keyValves:
            continue

        # Perform BFS
        distances[(v, v)] = 0
        q, d = deque([v]), 0
        while q:
            d += 1
            n = len(q)
            for _ in range(n):
                curV = q.popleft()
                for nextV in graph[curV].tunnels:
                    if (v, nextV) not in distances:
                        distances[(v, nextV)] = d
                        q.append(nextV)

    return distances


if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Time for part1', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Time for part2', e - s)
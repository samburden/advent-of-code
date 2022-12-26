import operator as op
from collections import deque
import time

class Monkey():

    lcm = 1
    def __init__(self, name, items, operator, opValue, testVal, monkeyIfTrue, monkeyIfFalse, reallyWorried=False):
        self.name = name
        self.queue = deque(items)
        self.operator = operator
        self.opValue = opValue
        self.testVal = testVal
        self.monkeyIfTrue = monkeyIfTrue
        self.monkeyIfFalse = monkeyIfFalse
        self.inspectionCount = 0
        self.reallyWorried = reallyWorried
        Monkey.lcm *= self.testVal


    def __str__(self):
        return f"Monkey:{self.name}, Operator:{self.operator}, OpValue:{self.opValue}, TestVal:{self.testVal}"

    def inspectNextItem(self):
        itemWorry = self.queue.popleft()
        if self.opValue == 'old':
            newWorry = self.getOperator(self.operator)(itemWorry, itemWorry)
        else:
            newWorry = self.getOperator(self.operator)(itemWorry, int(self.opValue))

        # For part one divide by 3, for part two mod by LCM of all divisors to keep worry small
        newWorry = newWorry // 3 if not self.reallyWorried else newWorry % Monkey.lcm

        if newWorry % self.testVal:
            newMonkey = self.monkeyIfFalse
        else:
            newMonkey = self.monkeyIfTrue
        self.inspectionCount += 1

        return newMonkey, newWorry
    def getOperator(self, operator):
        ops = {'+': op.add, '-': op.sub, '*': op.mul, '/': op.floordiv}
        return ops[operator]

def part1():
    monkeys = readMonkeys(False)

    print('Part 1:', runSimulation(monkeys, 20))


def part2():
    monkeys = readMonkeys(True)

    print('Part 2:', runSimulation(monkeys, 10000))

def readMonkeys(reallyWorried):
    monkeys = []
    with open('inputs/input11.txt') as f:
        while True:
            monkey = int(f.readline().strip().split()[1][0])
            itemsStr = f.readline().strip().split()[2:]
            items = []
            for i in itemsStr:
                items.append(int(i.replace(',', '')))
            operationStr = f.readline().strip().split()[4:]
            op, opVal = operationStr[0], operationStr[1]
            testVal = int(f.readline().strip().split()[-1])
            ifTrue = int(f.readline().strip().split()[-1])
            ifFalse = int(f.readline().strip().split()[-1])

            monkeys.append(Monkey(monkey, items, op, opVal, testVal, ifTrue, ifFalse, reallyWorried))
            if not f.readline():
                break

    return monkeys

def runSimulation(monkeys, rounds):
    for _ in range(rounds):
        for monkey in monkeys:
            for _ in range(len(monkey.queue)):
                newMonkey, newWorry = monkey.inspectNextItem()
                monkeys[newMonkey].queue.append(newWorry)

    num1, num2 = sorted([m.inspectionCount for m in monkeys], reverse=True)[:2]

    return num1 * num2

if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)
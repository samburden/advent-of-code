import time
import operator as op

class Monkey():

    def __init__(self, name, val=None, operation=None):
        self.name = name
        self.val = val
        self.operation = operation
        self.left = None
        self.right = None

    def __str__(self):
        return f"Monkey:{self.name}, Value:{self.value}, Operator:{self.operator}"

    def getOperator(self):
        ops = {'+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv, '=': op.eq}
        return ops[self.operation]


def part1():
    monkeys = buildMonkeys()
    print('Part 1:', int(findRootVal(monkeys['root'])))

def part2():
    monkeys = buildMonkeys()

    # Perform binary search checking possible humn values
    l, r = 0, 10000000000000
    while True:
        mid = l + (r - l) // 2
        monkeys['root'].operation = '='
        monkeys['humn'].val = mid

        if findRootVal(monkeys['root']):
            break
        if monkeys['root'].left.val > monkeys['root'].right.val:
            l = mid + 1
        else:
            r = mid - 1
        monkeys = buildMonkeys()

    print('Part 2:', monkeys['humn'].val)

def buildMonkeys():
    monkeys = {}
    with open('inputs/input21.txt') as f:
        for line in f:
            line = line.strip()
            if line:
                name, val, op, left, right = processLine(line)
                if name in monkeys:
                    m = monkeys[name]
                    m.val = val
                    m.operation = op
                else:
                    m = Monkey(name, val, op)
                    monkeys[name] = m

                if left:
                    m.left = Monkey(left) if left not in monkeys else monkeys[left]
                    monkeys[left] = m.left
                if right:
                    m.right = Monkey(right) if right not in monkeys else monkeys[right]
                    monkeys[right] = m.right
    return monkeys

def processLine(line):
    operators = {'+', '-', '*', '/'}
    monkeyTxt = line.split(':')
    name = monkeyTxt[0].strip()
    opMatch = next((op for op in operators if op in monkeyTxt[1]), False)
    if opMatch:
        return name, None, opMatch, monkeyTxt[1].strip()[:4], monkeyTxt[1].strip()[7:]
    else:
        return name, int(monkeyTxt[1].strip()), None, None, None


def findRootVal(node):
    if node.val:
        return node.val

    node.val = node.getOperator()(findRootVal(node.left), findRootVal(node.right))
    return node.val


if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)
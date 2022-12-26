import math
import time


class Node():
    def __init__(self, name, isFile=True, parent=None):
        self.name = name
        self.isFile = isFile
        self.size = 0
        self.children = []
        self.parent = parent


def part1():
    root = buildDirectory()
    ans = []
    dfs1(root, ans)

    print('Part 1:', sum(ans))


def part2():
    root = buildDirectory()
    totalSize = dfs1(root, [])
    print(totalSize)
    size = dfs2(root, 30000000-(70000000-totalSize))

    print('Part 2:', size)

def buildDirectory():
    root = Node('/', False)
    curNode = None
    with open('inputs/input7.txt') as f:
        for line in f:
            line = line.strip()
            # Check command
            if line.startswith('$'):
                commandArgs = line.split()
                cmd = commandArgs[1]
                if cmd == 'cd':
                    if commandArgs[2] == '/':
                        curNode = root
                    elif commandArgs[2] == '..':
                        curNode = curNode.parent
                    else:
                        newNode = Node(commandArgs[2], False, curNode)
                        curNode.children.append(newNode)
                        curNode = newNode
            else:
                output = line.split()
                if output[0] != 'dir':
                    newNode = Node(output[1], True, curNode)
                    newNode.size = int(output[0])
                    curNode.children.append(newNode)
    return root

def dfs1(node, ans):

    dirSize = 0
    for c in node.children:
        if c.isFile:
            dirSize += c.size
        else:
            dirSize += dfs1(c, ans)
    node.size = dirSize
    if dirSize <= 100000:
        ans.append(dirSize)
    return dirSize

def dfs2(node, neededFree):

    if node.size < neededFree:
        return math.inf

    ans = math.inf

    for c in node.children:
        if not c.isFile:
            ans = min(ans, dfs2(c, neededFree))

    if node.size >= neededFree and node.size < ans:
        ans = node.size

    return ans




if __name__ == '__main__':
    s = time.time()
    part1()
    e = time.time()
    print('Part 1 runtime:', e - s)
    s = time.time()
    part2()
    e = time.time()
    print('Part 2 runtime:', e - s)

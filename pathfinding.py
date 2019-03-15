import math
import sys

class Node:
    def __init__(self):
        self.position = ()
        self.content = ''
        cost = 0
        pred = 0

    def setPosition(self, position):
        self.position = position

    def setContent(self, content):
        self.content = content
    
    def setCost(self, cost):
        self.cost = cost
    
    def setPred(self, pred):
        self.pred = pred

    def getPosition(self):
        return self.position

    def getContent(self):
        return self.content

    def getCost(self):
        return self.cost

    def getPred(self):
        return self.pred
        

row = 0 # total number of row
col = 0 # total number of column
S = () # Star point
G = ()# End point
grid = []
input_file = "pathfinding_test.txt"
output_file_a = "pathfinding_a_out.txt"
output_file_b = "pathfinding_b_out.txt"

# node = [(row, col), content, cost, pred]

def getInputFile():
    global grid
    global row
    global col
    global input_file
    global S
    global G
    
    infile = open(input_file, "r" )
    grid = [[n for n in list(line)] for line in infile]
    row = len(grid)
    col = len(grid[row - 1])
    for i in range(row):
        for j in range(col):
            n = Node()
            n.setPosition((i + 1, j + 1))
            n.setContent(grid[i][j])
            n.setCost(math.inf)
            if grid[i][j] == 'S':
                S = (i + 1, j + 1)
                n.setCost(0)
                n.setPred(-1)
            elif grid[i][j] == 'G':
                G = (i + 1, j + 1)
            grid[i][j] = n
            
def writeOutFile_A(pendingStr):
    global outputFile
    with open(output_file_a, "a") as f:
        f.write(pendingStr + "\n")

def writeOutFile_B(pendingStr):
    global outputFile
    with open(output_file_b, "a") as f:
        f.write(pendingStr + "\n")

def pendingOutFile(grid, toReturn):
    global row
    global col
    
    for i in range(row):
        for j in range(col):
            toReturn += grid[i][j].getContent()
        toReturn += '\n'
    return toReturn

def find_4neighbours(node, reached, grid):
    position = node.getPosition()
    toReturn = []
    neighbours = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for i in range(4):
        neighbour = grid[position[0] + neighbours[i][0] - 1][position[1] + neighbours[i][1] - 1]
        if neighbour.getContent() != 'X':
            if not neighbour in reached:
                toReturn.append(neighbour)
    return toReturn

# find diagnal neighbours
def find_Dneighbours(node, reached, grid):
    position = node.getPosition()
    toReturn = []
    neighbours = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
    for i in range(8):
        neighbour = grid[position[0] + neighbours[i][0] - 1][position[1] + neighbours[i][1] - 1]
        if neighbour.getContent() != 'X':
            if not neighbour in reached:
                toReturn.append(neighbour)
    return toReturn

# Chebyshev heuristic
def Dh(node):
    global G
    position = node.getPosition()
    return max(abs(G[0] - position[0]), abs(G[1] - position[1]))

# Manhattan heuristic
def Mh(node):
    global G
    position = node.getPosition()
    return abs(G[0] - position[0]) + abs(G[1] - position[1])

def sort(queue):
    if len(queue) > 1:
        mid = len(queue) // 2
        L = queue[:mid]
        R = queue[mid:]

        sort(L)
        sort(R)

        i, j, k = 0, 0, 0

        while i < len(L) and j < len(R):
            if L[i].getCost() < R[j].getCost():
                queue[k] = L[i]
                i += 1
            else:
                queue[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            queue[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            queue[k] = R[j]
            j += 1
            k += 1
            
    return queue

def aStar_4():
    global row
    global col
    global grid
    global S
    global G

    result = grid

    queue = [result[S[0] - 1][S[1] - 1]]
    reached = []

    while queue:
        queue = sort(queue)
        current_node = queue[0]
        reached.append(current_node)
        queue.remove(current_node)
        neighbours = find_4neighbours(current_node, reached, result)
        for neighbour in neighbours:
            costX = current_node.getCost() + (1 + Mh(neighbour))
            costY = neighbour.getCost()
            if costX < costY:
                if costY == math.inf:
                    queue.append(neighbour)
                neighbour.setCost(costX)
                neighbour.setPred(current_node)

        if current_node.getContent() == 'G':
            current = current_node
            while current.getPred() != -1:
                if current.getContent() != 'G' and current.getContent() != 'S':
                    current.setContent('P')
                current = current.getPred()
    
    return result

def aStar_D():
    global row
    global col
    global grid
    global S
    global G

    result = grid

    queue = [result[S[0] - 1][S[1] - 1]]
    reached = []

    while queue:
        queue = sort(queue)
        current_node = queue[0]
        reached.append(current_node)
        queue.remove(current_node)
        neighbours = find_Dneighbours(current_node, reached, result)
        for neighbour in neighbours:
            costX = current_node.getCost() + (1 + Dh(neighbour))
            costY = neighbour.getCost()
            if costX < costY:
                if costY == math.inf:
                    queue.append(neighbour)
                neighbour.setCost(costX)
                neighbour.setPred(current_node)

        if current_node.getContent() == 'G':
            current = current_node
            while current.getPred() != -1:
                if current.getContent() != 'G' and current.getContent() != 'S':
                    current.setContent('P')
                current = current.getPred()
    
    return result

def greedy_4():
    global row
    global col
    global grid
    global S
    global G

    result = grid
    current_node = result[S[0] - 1][S[1] - 1]
    reached = []
    FOUND = 0

    while not FOUND:
        reached.append(current_node)
        neighbours = find_4neighbours(current_node, reached, result)
        for neighbour in neighbours:
            neighbour.setCost(Mh(neighbour))
        sort(neighbours)
        neighbours[0].setPred(current_node)
        current_node = neighbours[0]
        
        if current_node.getContent() == 'G':
            current = current_node
            while current.getPred() != -1:
                if current.getContent() != 'G' and current.getContent() != 'S':
                    current.setContent('P')
                current = current.getPred()
            FOUND = 1
        
    return result

def greedy_D():
    global row
    global col
    global grid
    global S
    global G

    result = grid
    current_node = result[S[0] - 1][S[1] - 1]
    reached = []
    FOUND = 0

    while not FOUND:
        reached.append(current_node)
        neighbours = find_Dneighbours(current_node, reached, result)
        for neighbour in neighbours:
            neighbour.setCost(Dh(neighbour))
        sort(neighbours)
        neighbours[0].setPred(current_node)
        current_node = neighbours[0]
        
        if current_node.getContent() == 'G':
            current = current_node
            while current.getPred() != -1:
                if current.getContent() != 'G' and current.getContent() != 'S':
                    current.setContent('P')
                current = current.getPred()
            FOUND = 1
        
    return result
        
        
        


def main():
    global row
    global col
    global grid
    global S
    global G

    pendingOut_a = "Greedy\n"
    pendingOut_b = "Greedy\n"
        
    getInputFile()

    print("start Greedy")
    pendingOut_a = pendingOutFile(greedy_4(), pendingOut_a)
    pendingOut_b = pendingOutFile(greedy_D(), pendingOut_b)
    print("end Greedy")

    pendingOut_a += "\nA*\n"
    pendingOut_b += "\nA*\n"
    
    print("start A*")
    pendingOut_a = pendingOutFile(aStar_4(), pendingOut_a)
    pendingOut_b = pendingOutFile(aStar_D(), pendingOut_b)
    print("end A*")
    writeOutFile_A(pendingOut_a)
    writeOutFile_B(pendingOut_b)
    
    return



main()

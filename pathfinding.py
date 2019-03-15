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
        

rowA = 0 # total number of row
colA = 0 # total number of column
SA = () # Star point
GA = ()# End point
rowB = 0 # total number of row
colB = 0 # total number of column
SB = () # Star point
GB = ()# End point
gridA = []
gridB = []
input_file_a = "pathfinding_a.txt"
input_file_b = "pathfinding_b.txt"
output_file_a = "pathfinding_a_out.txt"
output_file_b = "pathfinding_b_out.txt"

# node = [(row, col), content, cost, pred]

def getInputFile():
    global gridA
    global rowA
    global colA
    global gridB
    global rowB
    global colB
    global input_file_a
    global input_file_b
    global SA
    global GA
    global SB
    global GB
    
    infile = open(input_file_a, "r" )
    gridA = [[n for n in list(line)] for line in infile]
    rowA = len(gridA)
    colA = len(gridA[rowA - 1])
    for i in range(rowA):
        for j in range(colA):
            n = Node()
            n.setPosition((i + 1, j + 1))
            n.setContent(gridA[i][j])
            n.setCost(math.inf)
            if gridA[i][j] == 'S':
                SA = (i + 1, j + 1)
                n.setCost(0)
                n.setPred(-1)
            elif gridA[i][j] == 'G':
                GA = (i + 1, j + 1)
            gridA[i][j] = n

    infile = open(input_file_b, "r" )
    gridB = [[n for n in list(line)] for line in infile]
    rowB = len(gridB)
    colB = len(gridB[rowB - 1])
    for i in range(rowB):
        for j in range(colB):
            n = Node()
            n.setPosition((i + 1, j + 1))
            n.setContent(gridB[i][j])
            n.setCost(math.inf)
            if gridB[i][j] == 'S':
                SB = (i + 1, j + 1)
                n.setCost(0)
                n.setPred(-1)
            elif gridB[i][j] == 'G':
                GB = (i + 1, j + 1)
            gridB[i][j] = n

            
            
def writeOutFile_A(pendingStr):
    global outputFile
    with open(output_file_a, "a") as f:
        f.write(pendingStr + "\n")

def writeOutFile_B(pendingStr):
    global outputFile
    with open(output_file_b, "a") as f:
        f.write(pendingStr + "\n")

def pendingOutFile_A(grid, toReturn):
    global rowA
    global colA
    
    for i in range(rowA):
        for j in range(colA):
            toReturn += grid[i][j].getContent()
        toReturn += '\n'
    return toReturn

def pendingOutFile_B(grid, toReturn):
    global rowB
    global colB
    
    for i in range(rowB):
        for j in range(colB):
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
    global GB
    position = node.getPosition()
    return max(abs(GB[0] - position[0]), abs(GB[1] - position[1]))

# Manhattan heuristic
def Mh(node):
    global GA
    position = node.getPosition()
    return abs(GA[0] - position[0]) + abs(GA[1] - position[1])

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
    global rowA
    global colA
    global gridA
    global SA
    global GA

    result = gridA

    queue = [result[SA[0] - 1][SA[1] - 1]]
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
    global rowB
    global colB
    global gridB
    global SB
    global GB

    result = gridB

    queue = [result[SB[0] - 1][SB[1] - 1]]
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
    global rowA
    global colA
    global gridA
    global SA
    global GA

    result = gridA
    current_node = result[SA[0] - 1][SA[1] - 1]
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
    global rowB
    global colB
    global gridB
    global SB
    global GB

    result = gridB
    current_node = result[SB[0] - 1][SB[1] - 1]
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
    global rowA
    global colA
    global gridA
    global SA
    global GA
    global rowB
    global colB
    global gridB
    global SB
    global GB

    pendingOut_a = "Greedy\n"
    pendingOut_b = "Greedy\n"
        
    getInputFile()

    print("start Greedy")
    pendingOut_a = pendingOutFile_A(greedy_4(), pendingOut_a)
    pendingOut_b = pendingOutFile_B(greedy_D(), pendingOut_b)
    print("end Greedy")

    getInputFile()
    
    pendingOut_a += "\nA*\n"
    pendingOut_b += "\nA*\n"
    
    print("start A*")
    pendingOut_a = pendingOutFile_A(aStar_4(), pendingOut_a)
    pendingOut_b = pendingOutFile_B(aStar_D(), pendingOut_b)
    print("end A*")

    #print(pendingOut_a)
    #print(pendingOut_b)
    
    writeOutFile_A(pendingOut_a)
    writeOutFile_B(pendingOut_b)
    
    return



main()

import os
import sys
import heapq
import math
import time

# from copy import copy, deepcopy

class Node:
    current_state = []
    directions = []
    eDist = 0

    def __init__(self, state, dir):
        self.current_state = state
        self.directions = dir
        self.mhDist = euclidean_dist(self)

    def __lt__(self, other): 
        if(self.eDist < other.eDist): 
            return True
        else: 
            return False

def euclidean_dist(nNode):
    state = nNode.current_state
    size = len(state)
    nNode.eDist = 0
    for row in range(size):
        for col in range(size):
            val = state[row][col]
            if val == 0:
                r_col = size - 1
                r_row = size - 1
            else:
                r_col = (val - 1) % size
                r_row = (val - 1) // size
            nNode.eDist += math.sqrt((r_row - row)**2 + (r_col - col)**2)

def print_state(state):
    ele = ''
    for innerList in state:
        for singleElement in innerList:
            ele += str(singleElement) + " "
        ele += "\n"

def hash_state(state):
    ele = ''
    for innerList in state:
        for singleElement in innerList:
            ele += str(singleElement) + " "
        ele += "\n"
    return ele

def swapPositions(old, pos1x, pos1y, pos2x, pos2y):
    copy = [row[:] for row in old]
    val = copy[pos1x][pos1y]
    copy[pos1x][pos1y] = copy[pos2x][pos2y]
    copy[pos2x][pos2y] = val
    return copy

def format_moves(directions):
    new_directions = []
    for i in directions:
        if i == 0:
            new_directions.append("Left")
        elif i == 1:
            new_directions.append("Right")
        elif i == 2:
            new_directions.append("Up")
        elif i == 3:
            new_directions.append("Down")
    return new_directions

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()

    def generate_neighbours(self, cNode, visited):
        row = cNode.zero_pos[0]
        col = cNode.zero_pos[1]
        size = len(cNode.current_state)

        returnArr = []
        dirs = [[-1, 0, 0], [0, -1, 1], [1, 0, 2], [0, 1, 3]]
        for dir in dirs:
            checkRow = row + dir[0]
            checkCol = col + dir[1]
            if checkRow < 0 or checkRow > size - 1 or checkCol < 0 or checkCol > size - 1:
                continue
            newNeighbour = swapPositions(cNode.current_state, checkRow, checkCol, row, col)

            newZeroPos = [checkRow, checkCol]

            newDirections = cNode.directions[:]
            newDirections.append(dir[2])
            nNode = Node(newNeighbour, newDirections, newZeroPos)

            # check if new neighbour is not solvable, then don't add to list
            # if not is_solvable(nNode):
            #     continue

            manhattan_dist_linear_update_with_linear_conflicts(nNode, cNode)

            returnArr.append(nNode)

        return returnArr

    def solve(self):
        start = time.time()
        #TODO
        # implement your search algorithm here
        visited = set()
        frontier = []

        # using priority queue
        heapq.heapify(frontier)

        directions = []
        mNode = Node(init_state, directions)
        
        heapq.heappush(frontier, (mNode.eDist, mNode))
        
        #frontier.append(mNode)
        goal_found = False
        
        goal_state_str = hash_state(goal_state)
        #while len(frontier) != 0:
        while frontier:
            #cNode = frontier.pop(0)
            cNode = heapq.heappop(frontier)[1]
            current_state = cNode.current_state
            search_state_str = hash_state(current_state)
            visited.add(search_state_str)
            if search_state_str == goal_state_str:
                goal_found = True
                directions = format_moves(cNode.directions)
                break
            else:
                neighbours = self.generate_neighbours(cNode)
                for nNode in neighbours:
                    parsed_state = hash_state(nNode.current_state)
                    if parsed_state not in visited:
                        #print(nNode.mhDist)
                        #frontier.append(nNode)
                        heapq.heappush(frontier, (nNode.eDist + len(nNode.directions), nNode))

        if goal_found:
            print('Took ', time.time() - start)
            print(directions)
            return directions
        else:
            print('Took ', time.time() - start)
            directions.append("UNSOLVABLE")
            print(directions)
            return directions

if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()
    
    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]
    

    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')

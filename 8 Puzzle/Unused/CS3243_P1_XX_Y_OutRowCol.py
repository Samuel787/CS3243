import os
import sys
import heapq
import math

# from copy import copy, deepcopy

class Node:
    current_state = []
    directions = []
    wDist = 0

    def __init__(self, state, dir):
        self.current_state = state
        self.directions = dir
        self.mhDist = wrong_col_row_dist(self)

    def __lt__(self, other): 
        if(self.wDist < other.wDist): 
            return True
        else: 
            return False

# number of values that are in the wrong row + 
# number of values that are in the wrong col
def wrong_col_row_dist(nNode):
    state = nNode.current_state
    size = len(state)
    nNode.wDist = 0
    for row in range(size):
        for col in range(size):
            val = state[row][col]
            if val == 0:
                r_col = size - 1
                r_row = size - 1
            else:
                r_col = (val - 1) % size
                r_row = (val - 1) // size
            if r_col != col:
                nNode.wDist += 1
            if r_row != row:
                nNode.wDist += 1

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

def deep_copy_Node(oNode):
    nNode = Node([row[:] for row in oNode.current_state], oNode.directions[:])
    return nNode

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

    def generate_neighbours(self, cNode):
        row = -1
        col = -1
        flag = False
        curr_state = cNode.current_state
        size = len(curr_state)


        for i in range(size):
            for j in range(size):
                if curr_state[i][j] == 0:
                    row = i
                    col = j

        neighbours = []
        for i in range(4):
            if i == 0:
                # Move Left
                if col == size - 1:
                    continue
                else:
                    nNode = deep_copy_Node(cNode)
                    nState = nNode.current_state
                    nState[row][col], nState[row][col + 1] = nState[row][col + 1], nState[row][col]
                    # print("left", nNode.current_state)
                    nNode.directions.append(0)
                    wrong_col_row_dist(nNode)
                    neighbours.append(nNode)
            elif i == 1:
                # Move Right
                if col == 0:
                    continue
                else:
                    nNode = deep_copy_Node(cNode)
                    nState = nNode.current_state
                    nState[row][col], nState[row][col - 1] = nState[row][col - 1], nState[row][col]
                    # print("right", nNode.current_state)
                    nNode.directions.append(1)
                    wrong_col_row_dist(nNode)
                    neighbours.append(nNode)
            elif i == 2:
                # Move Up
                if row == size - 1:
                    continue
                else:
                    nNode = deep_copy_Node(cNode)
                    nState = nNode.current_state
                    nState[row][col], nState[row + 1][col] = nState[row + 1][col], nState[row][col]
                    # print("up", nNode.current_state)
                    nNode.directions.append(2)
                    wrong_col_row_dist(nNode)
                    neighbours.append(nNode)
            elif i == 3:
                # Move Down
                if row == 0:
                    continue
                else:
                    nNode = deep_copy_Node(cNode)
                    nState = nNode.current_state
                    nState[row][col], nState[row - 1][col] = nState[row - 1][col], nState[row][col]
                    # print("down", nNode.current_state)
                    nNode.directions.append(3)
                    wrong_col_row_dist(nNode)
                    neighbours.append(nNode)
        return neighbours

    def solve(self):
        #TODO
        # implement your search algorithm here
        visited = set()
        frontier = []

        # using priority queue
        heapq.heapify(frontier)

        directions = []
        mNode = Node(init_state, directions)
        
        heapq.heappush(frontier, (mNode.wDist, mNode))
        
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
                        heapq.heappush(frontier, (nNode.wDist + len(nNode.directions), nNode))

        if goal_found:
            print(directions)
            return directions
        else:
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
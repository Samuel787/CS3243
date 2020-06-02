import math
import os
import sys
import heapq
import time

x_start = []
y_start = []

class Node:
    current_state = []
    directions = []
    euDist = 0
    zero_pos = []

    def __init__(self, state, dir, zero_pos):
        self.current_state = state
        self.directions = dir
        self.zero_pos = zero_pos

    def __lt__(self, other):
        if (self.euDist < other.euDist):
            return True
        else:
            return False

def set_starts(init_state):
    size = len(init_state)
    for i in range (9):
        x_start.append(0)
        y_start.append(0)
    
    for y in range(size):
        for x in range(size):
            x_start[init_state[y][x]] = x
            y_start[init_state[y][x]] = y

def euclidean_dist(nNode):
    state = nNode.current_state
    size = len(state)
    nNode.euDist = 0
    for row in range(size):
        for col in range(size):
            val = state[row][col]
            if val == 0:
                # r_col = size - 1
                # r_row = size - 1
                continue
            else:
                r_col = (val - 1) % size
                r_row = (val - 1) // size
                dx1 = col - r_col
                dx2 = x_start[val] - 

            nNode.euDist += math.sqrt((r_row - row)**2 + (r_col - col)**2)

def euclidean_dist_linear_update(nNode, cNode):
    size = len(cNode.current_state)

    # val represents the value swapped with zero
    val = cNode.current_state[nNode.zero_pos[0]][nNode.zero_pos[1]]

    # goal position for val
    goal_row_val = (val - 1) // size
    goal_col_val = (val - 1) % size

    # positions for value
    old_pos_val = nNode.zero_pos
    new_pos_val = cNode.zero_pos

    # get old and new euclidean value for val
    old_eu_val = math.sqrt((goal_row_val - old_pos_val[0])**2 + (goal_col_val - old_pos_val[1])**2)
    new_eu_val = math.sqrt((goal_row_val - new_pos_val[0])**2 + (goal_col_val - new_pos_val[1])**2)

    # positions for zero
    old_pos_zero = cNode.zero_pos
    new_pos_zero = nNode.zero_pos

    # goal position for zero
    goal_row_zero = size - 1
    goal_col_zero = size - 1

    #get old and new euclidean value for zero
    old_eu_zero = math.sqrt((goal_row_zero - old_pos_zero[0])**2 + (goal_col_zero - old_pos_zero[1])**2)
    new_eu_zero = math.sqrt((goal_row_zero - new_pos_zero[0])**2 + (goal_col_zero - new_pos_zero[1])**2)

    nNode.euDist = cNode.euDist - old_eu_val - old_eu_zero + new_eu_val + new_eu_zero

def proper_str_state(state):
    ele = ''
    for innerList in state:
        for singleElement in innerList:
            ele += str(singleElement) + " "
        ele += "\n"
    return ele

def hash_state(state):
    return hash(str(state))

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
        self.init_state = init_state
        self.goal_state = goal_state

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

            # euclidean_dist_linear_update(nNode, cNode)
            euclidean_dist(nNode)
            returnArr.append(nNode)

        return returnArr

    def solve(self):
        start = time.time()
        f = False

        row = -1
        col = -1
        size = len(self.init_state)
        for i in range(size):
            for j in range(size):
                if self.init_state[i][j] == 0:
                    row = i
                    col = j
                    f = True
                    break
            if f:
                break

        visited = set()
        frontier = []

        heapq.heapify(frontier)

        directions = []
        mNode = Node(self.init_state, directions, [row, col])
        euclidean_dist(mNode)
        heapq.heappush(frontier, (mNode.euDist, mNode))

        goal_found = False

        goal_state_str = hash_state(self.goal_state)

        while frontier:
            cNode = heapq.heappop(frontier)[1]
            current_state = cNode.current_state
            search_state_str = hash_state(current_state)
            visited.add(search_state_str)
            if search_state_str == goal_state_str:
                goal_found = True
                directions = format_moves(cNode.directions)
                break
            else:
                neighbours = self.generate_neighbours(cNode, visited)

                for nNode in neighbours:
                    parsed_state = hash_state(nNode.current_state)
                    if parsed_state not in visited:
                        heapq.heappush(frontier, (nNode.euDist + len(nNode.directions), nNode))

        time_taken = time.time() - start

        if goal_found:
            print('Took ', time_taken)
            print(directions)
            return directions
        else:
            print('Took ', time_taken)
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

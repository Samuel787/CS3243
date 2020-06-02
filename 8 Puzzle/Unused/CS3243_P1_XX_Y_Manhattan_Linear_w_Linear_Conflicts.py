import os
import sys
import heapq
import time

class Node:
    current_state = []
    directions = []
    mhDist = 0
    zero_pos = []

    def __init__(self, state, dir, zero_pos):
        self.current_state = state
        self.directions = dir
        self.zero_pos = zero_pos

    def __lt__(self, other):
        if (self.mhDist < other.mhDist):
            return True
        else:
            return False

def manhattan_dist_with_linear_conflict(nNode):
    state = nNode.current_state
    size = len(state)
    nNode.mhDist = 0
    for row in range(size):
        for col in range(size):
            val = state[row][col]
            linear_conflicts = 0
            if val == 0:
                r_row = size - 1
                r_col = size - 1
            else:
                r_row = (val - 1) // size
                r_col = (val - 1) % size

                if (r_row == row and r_col != col) or (r_row != row and r_col == col):
                    other_val = state[r_row][r_col]
                    other_val_goal_row = (other_val - 1) // size
                    other_val_goal_col = (other_val - 1) % size
                    if other_val_goal_row == row and other_val_goal_col == col:
                        linear_conflicts += 1
            nNode.mhDist += abs(r_row - row) + abs(r_col - col) + linear_conflicts

def manhattan_dist_linear_update_with_linear_conflicts(nNode, cNode):
    # value swapped with zero
    val = cNode.current_state[nNode.zero_pos[0]][nNode.zero_pos[1]]
    size = len(nNode.current_state)

    val_goal_row = (val - 1) // size
    val_goal_col = (val - 1) % size

    val_old_pos = nNode.zero_pos
    val_new_pos = cNode.zero_pos

    old_mh_dist_for_val = abs(val_goal_row - val_old_pos[0]) + abs(val_goal_col - val_old_pos[1])
    new_mh_dist_for_val = abs(val_goal_row - val_new_pos[0]) + abs(val_goal_col - val_new_pos[1])

    # update mh dist for value swapped with zero
    nNode.mhDist = cNode.mhDist - old_mh_dist_for_val + new_mh_dist_for_val

    zero_goal_row = size - 1
    zero_goal_col = size - 1

    zero_old_pos = cNode.zero_pos
    zero_new_pos = nNode.zero_pos

    old_mh_dist_for_zero = abs(zero_goal_row - zero_old_pos[0]) + abs(zero_goal_col - zero_old_pos[1])
    new_mh_dist_for_zero = abs(zero_goal_row - zero_new_pos[0]) + abs(zero_goal_col - zero_new_pos[1])

    # update mh dist for zero
    nNode.mhDist = nNode.mhDist - old_mh_dist_for_zero + new_mh_dist_for_zero

    # handling linear conflict differences

    # check if old pos for val has linear conflict
    if val_goal_row == val_old_pos[0] or val_goal_col == val_old_pos[1]:
        possible_conflict_val = cNode.current_state[val_goal_row][val_goal_col]

        # check that value at val_goal_pos is not zero and not itself
        if possible_conflict_val > 0 and possible_conflict_val != val:
            possible_conflict_goal_row = (possible_conflict_val - 1) // size
            possible_conflict_goal_col = (possible_conflict_val - 1) % size

            # check that goal position of possible conflict is the same as val_old_pos
            if possible_conflict_goal_row == val_old_pos[0] and possible_conflict_goal_col == val_old_pos[1]:
                nNode.mhDist -= 2

    # check if new pos for val has linear conflict
    elif val_goal_row == val_new_pos[0] or val_goal_col == val_new_pos[1]:
        possible_conflict_val = nNode.current_state[val_goal_row][val_goal_col]

        # check that value at val_goal_pos is not zero and not itself
        if possible_conflict_val > 0 and possible_conflict_val != val:
            possible_conflict_goal_row = (possible_conflict_val - 1) // size
            possible_conflict_goal_col = (possible_conflict_val - 1) % size

            #check that goal position of possible conflict is the same as the val_new_pos
            if possible_conflict_goal_row == val_new_pos[0] and possible_conflict_goal_col == val_new_pos[1]:
                nNode.mhDist += 2


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

            manhattan_dist_linear_update_with_linear_conflicts(nNode, cNode)

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
        manhattan_dist_with_linear_conflict(mNode)
        heapq.heappush(frontier, (mNode.mhDist, mNode))

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
                        heapq.heappush(frontier, (nNode.mhDist + len(nNode.directions), nNode))

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

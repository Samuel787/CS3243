import os
import sys
import heapq
import time

from copy import copy, deepcopy

class Node:
    current_state = []
    # directions = []
    mhDist = 0
    zero_pos = []

    # def __init__(self, state, dir, zero_pos):
    def __init__(self, state, zero_pos):
        self.current_state = state
        # self.directions = dir
        self.zero_pos = zero_pos

    def __lt__(self, other):
        if (self.mhDist < other.mhDist):
            return True
        else:
            return False

def mhDist(state):
    size = len(state)
    mhDist = 0
    for row in range(size):
        for col in range(size):
            val = state[row][col]
            if val == 0:
                # r_row = size - 1
                # r_col = size - 1
                continue
            else:
                r_row = (val - 1) // size
                r_col = (val - 1) % size
            mhDist += abs(r_row - row) + abs(r_col - col)
    print (mhDist)
        
def manhattan_dist_with_linear_conflict(nNode):
    state = nNode.current_state
    size = len(state)
    nNode.mhDist = 0
    for row in range(size):
        for col in range(size):
            val = state[row][col]
            linear_conflicts = 0
            if val == 0:
                # r_row = size - 1
                # r_col = size - 1
                continue
            else:
                r_row = (val - 1) // size
                r_col = (val - 1) % size

                # calculate linear conflicts
                if (r_row == row and r_col != col) or (r_row != row and r_col == col):
                    other_val = state[r_row][r_col]
                    other_val_goal_row = (other_val - 1) // size
                    other_val_goal_col = (other_val - 1) % size
                    if other_val_goal_row == row and other_val_goal_col == col:
                        linear_conflicts += 1
            # nNode.mhDist += abs(r_row - row) + abs(r_col - col) + linear_conflicts
            nNode.mhDist += abs(r_row - row) + abs(r_col - col)

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
    # nNode.mhDist = cNode.mhDist - old_mh_dist_for_val + new_mh_dist_for_val

    # zero_goal_row = size - 1
    # zero_goal_col = size - 1

    # zero_old_pos = cNode.zero_pos
    # zero_new_pos = nNode.zero_pos

    # old_mh_dist_for_zero = abs(zero_goal_row - zero_old_pos[0]) + abs(zero_goal_col - zero_old_pos[1])
    # new_mh_dist_for_zero = abs(zero_goal_row - zero_new_pos[0]) + abs(zero_goal_col - zero_new_pos[1])

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


def is_solvable(mNode):
    size = len(mNode.current_state)
    inv_count = get_inv_count(mNode)

    # size is odd
    if size % 2 != 0:
        # inv_count is even
        if inv_count % 2 == 0:
            return True
    # size is even
    else:
        # zero on an even indexed row
        if mNode.zero_pos[0] % 2 == 0:
            # inv_count is odd
            if inv_count % 2 != 0:
                return True
        # zero on an odd indexed row
        else:
            # inv_count is even
            if inv_count % 2 == 0:
                return True


    return False

def get_inv_count(mNode):
    flattern = []
    size = len(mNode.current_state)
    for row in range(size):
        for col in range(size):
            if mNode.current_state[row][col] == 0:
                zero_pos = (size * row) + col
            flattern.append(mNode.current_state[row][col])

    size_arr = len(flattern)

    inv_count = mergeSort(flattern, size_arr) - zero_pos
    # print inv_count

    return inv_count

# Function to Use Inversion Count
def mergeSort(arr, n):
    # A temp_arr is created to store
    # sorted array in merge function
    temp_arr = [0]*n
    return _mergeSort(arr, temp_arr, 0, n-1)

# This Function will use MergeSort to count inversions

def _mergeSort(arr, temp_arr, left, right):

    # A variable inv_count is used to store
    # inversion counts in each recursive call

    inv_count = 0

    # We will make a recursive call if and only if
    # we have more than one elements

    if left < right:

        # mid is calculated to divide the array into two subarrays
        # Floor division is a must in case of python

        mid = (left + right) // 2

        # It will calculate inversion counts in the left subarray

        inv_count += _mergeSort(arr, temp_arr, left, mid)

        # It will calculate inversion counts in right subarray

        inv_count += _mergeSort(arr, temp_arr, mid + 1, right)

        # It will merge two subarrays in a sorted subarray

        inv_count += merge(arr, temp_arr, left, mid, right)
    return inv_count

# This function will merge two subarrays in a single sorted subarray
def merge(arr, temp_arr, left, mid, right):
    i = left     # Starting index of left subarray
    j = mid + 1 # Starting index of right subarray
    k = left     # Starting index of to be sorted subarray
    inv_count = 0

    # Conditions are checked to make sure that i and j don't exceed their
    # subarray limits.

    while i <= mid and j <= right:

        # There will be no inversion if arr[i] <= arr[j]

        if arr[i] <= arr[j]:
            temp_arr[k] = arr[i]
            k += 1
            i += 1
        else:
            # Inversion will occur.
            temp_arr[k] = arr[j]
            inv_count += (mid-i + 1)
            k += 1
            j += 1

    # Copy the remaining elements of left subarray into temporary array
    while i <= mid:
        temp_arr[k] = arr[i]
        k += 1
        i += 1

    # Copy the remaining elements of right subarray into temporary array
    while j <= right:
        temp_arr[k] = arr[j]
        k += 1
        j += 1

    # Copy the sorted subarray into Original array
    for loop_var in range(left, right + 1):
        arr[loop_var] = temp_arr[loop_var]

    return inv_count


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

# def opposite_direction (mNode):
#     copy = [row[:] for row in mNode[0].current_state]
#     zero_pos = mNode[0].zero_pos
#     i = mNode[1][2]
#     if i == 0:
#         # print ("Left")
#         # Originally Going Left
#         copy[zero_pos[0]][zero_pos[1]] = copy[zero_pos[0]][zero_pos[1] - 1]
#         copy[zero_pos[0]][zero_pos[1] - 1] = 0
#     elif i == 1:
#         print ("Right")
#         # Originally Going Right
#         copy[zero_pos[0]][zero_pos[1]] = copy[zero_pos[0]][zero_pos[1] + 1]
#         copy[zero_pos[0]][zero_pos[1] + 1] = 0
#     elif i == 2:
#         print ("Up")
#         # Originally Going Up
#         copy[zero_pos[0]][zero_pos[1]] = copy[zero_pos[0] - 1][zero_pos[1]]
#         copy[zero_pos[0] - 1][zero_pos[1]] = 0
#     elif i == 3:
#         print ("Down")
#         # Originally Going Down
#         copy[zero_pos[0]][zero_pos[1]] = copy[zero_pos[0] + 1][zero_pos[1]]
#         copy[zero_pos[0] + 1][zero_pos[1]] = 0
    
#     print()
#     return copy

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        self.init_state = init_state
        self.goal_state = goal_state

    def generate_neighbours(self, cNode):
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

            # newDirections = cNode.directions[:]
            # newDirections.append(dir[2])
            nNode = Node(newNeighbour, newZeroPos)
            # nNode = Node(newNeighbour, newDirections, newZeroPos)

            # manhattan_dist_linear_update_with_linear_conflicts(nNode, cNode)
            manhattan_dist_with_linear_conflict(nNode)
<<<<<<< HEAD:CS3243_P1_XX_Y_Manhattan_Linear_w_Linear_Conflicts_w_Inv_Count_Init.py
            returnArr.append(nNode)
        
=======
            returnArr.append([nNode, dir])

>>>>>>> 2806210eb53aad23d5dec48713cb52227cd3441f:Unused/uninformed_bfs.py
        return returnArr

    def solve(self):
        f = False
        start = time.time()

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

        g = {}
        g[tuple(map(tuple, self.init_state))] = 0

        prev = {}
        prev[tuple(map(tuple, self.init_state))] = -1

        dirs = {}
        prev[tuple(map(tuple, self.init_state))] = -1


        heapq.heapify(frontier)

        directions = []
        mNode = Node(self.init_state, [row, col])
        # mNode = Node(self.init_state, directions, [row, col])

        # check if its solvable
        if not is_solvable(mNode):
            # print('Took ', time.time() - start)
            directions.append("UNSOLVABLE")
            print(directions)
            return directions

        manhattan_dist_with_linear_conflict(mNode)
        heapq.heappush(frontier, (mNode.mhDist, mNode))

        start = time.time()

        while frontier:
            cNode = heapq.heappop(frontier)[1]
            current_state = cNode.current_state
            current_parsed_state = tuple(map(tuple, cNode.current_state))

            if current_parsed_state in visited:
                continue

            visited.add(tuple(map(tuple, current_state)))
            if current_state == self.goal_state:
                # directions = format_moves(cNode.directions)
                break
            else:
                neighbours = self.generate_neighbours(cNode)
                for nNode in neighbours:
                    parsed_state = tuple(map(tuple, nNode[0].current_state))
                    if parsed_state in visited:
                        continue

                    if parsed_state not in g or g[current_parsed_state] + 1 < g[parsed_state]:
                        prev[parsed_state] = current_parsed_state
                        dirs[parsed_state] = nNode[1]
                        g[parsed_state] = g[current_parsed_state] + 1
<<<<<<< HEAD:CS3243_P1_XX_Y_Manhattan_Linear_w_Linear_Conflicts_w_Inv_Count_Init.py
                        heapq.heappush(frontier, (g[p  arsed_state] + nNode.mhDist, nNode))
=======
                        heapq.heappush(frontier, (g[parsed_state] + nNode[0].mhDist, nNode[0]))
>>>>>>> 2806210eb53aad23d5dec48713cb52227cd3441f:Unused/uninformed_bfs.py

                    # if parsed_state not in visited:
                    #     heapq.heappush(frontier, (nNode.mhDist + len(nNode.directions), nNode))

        time_taken = time.time() - start
        print('Took ', time_taken)
        # Start backtracing
        v = tuple(map(tuple, self.goal_state))
        finalDirections = []
        while (prev[v] != -1): 
            finalDirections.append(dirs[v][2])
            v = tuple(map(tuple, prev[v]))
        print(format_moves(finalDirections[::-1]))

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

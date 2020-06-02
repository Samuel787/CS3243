import os
import sys
import time

class Node:
    current_state = []
    zero_pos = []

    def __init__(self, state, zero_pos):
        self.current_state = state
        self.zero_pos = zero_pos

#region Util Function
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
#endregion

#region Solvable
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
#endregion

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        self.init_state = init_state
        self.goal_state = goal_state
        self.nodes_expanded = 0
        self.time_taken = 0
        
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
            nNode = Node(newNeighbour, newZeroPos)
            returnArr.append([nNode, dir])
        return returnArr

    def solve(self):
        #region Find Zero Pos
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
        #endregion

        #region Define Variables
        visited = set()
        frontier = []
        directions = []

        prev = {}
        prev[tuple(map(tuple, self.init_state))] = -1

        dirs = {}
        prev[tuple(map(tuple, self.init_state))] = -1
        #endregion 


        # Create first node and append to frontier
        mNode = Node(self.init_state, [row, col])
        frontier.append([mNode, [-1]])

        #region Check if its solvable
        if not is_solvable(mNode):
            directions.append("UNSOLVABLE")
            print(directions)
            return directions
        #endregion 

        start = time.time()
        while len(frontier) > 0:
            cNode = frontier.pop(0)[0]
            current_state = cNode.current_state
            current_parsed_state = tuple(map(tuple, cNode.current_state))
            visited.add(current_parsed_state)
            self.nodes_expanded += 1

            if current_state == self.goal_state:
                break
            else:
                neighbours = self.generate_neighbours(cNode)
                for nNode in neighbours:
                    parsed_state = tuple(map(tuple, nNode[0].current_state))
                    if parsed_state not in visited:
                        prev[parsed_state] = current_parsed_state
                        dirs[parsed_state] = nNode[1]
                        frontier.append(nNode)

        self.time_taken = time.time() - start
        print('Took:', self.time_taken)
        print('Nodes:', self.nodes_expanded)

        # Start backtracing
        v = tuple(map(tuple, self.goal_state))
        finalDirections = []
        while (prev[v] != -1): 
            finalDirections.append(dirs[v][2])
            v = tuple(map(tuple, prev[v]))
        directions = format_moves(finalDirections[::-1])
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
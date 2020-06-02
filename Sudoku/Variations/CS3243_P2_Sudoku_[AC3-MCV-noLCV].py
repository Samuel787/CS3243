import sys
import copy
from collections import deque
import time
# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

def convert_81(r, c):
    return 9 * r + c

def generate_neighbours(row, col):
    neighbours = []
    for i in range(81):
        neighbours.append(set())
    pos = convert_81(row, col)
    for i in range(9):
        for j in range(9):
            if pos != convert_81(i, j) and (row == i or col == j):
                neighbours[pos].add(convert_81(i, j))
    for i in range((row // 3) * 3, (row // 3) * 3 + 3):
        for j in range((col // 3) * 3, (col // 3) * 3 + 3):
            if convert_81(i , j) != pos:
                neighbours[pos].add(convert_81(i, j))
    return neighbours   

def calculate_domain(state, position):
    domain = set([1, 2, 3, 4, 5, 6, 7, 8, 9])

    row_idx = position[0]
    col_idx = position[1]

    for i in range(9):
        current_value_row = state[row_idx][i]  # check same row
        if current_value_row != 0:
            domain.discard(current_value_row)

        current_value_col = state[i][col_idx]  # check same col
        if current_value_col != 0:
            domain.discard(current_value_col)

    # check subgrid
    subgrid_topleft_idx = (row_idx//3 * 3, col_idx//3 * 3)
    x = subgrid_topleft_idx[0]
    y = subgrid_topleft_idx[1]
    for i in range(3):
        for j in range(3):
            current_value_subgrid = state[i+x][j+y]
            if current_value_subgrid != 0 :
                domain.discard(current_value_subgrid)

    return domain

def sort_by_least_constrained_value(state, domain, position):
    to_be_sorted = []

    for val in domain:
        no_of_possible_val_for_other_boxes = 0

        # insert val into state
        new_state = copy.deepcopy(state)
        x = position[0]
        y = position[1]
        new_state[x][y] = val

        # calculate the total number of possible val for other boxes
        for i in range(9):
            for j in range(9):
                curr_position = (i, j)
                if new_state[i][j] != 0:
                    no_of_possible_val_for_other_boxes += 1
                else:
                    no_of_possible_val_for_other_boxes += len(calculate_domain(new_state, curr_position))

        # add a tuple of (value, metric of how constraining is this value)
        to_be_sorted.append((val, no_of_possible_val_for_other_boxes))

    to_be_sorted.sort(key = lambda x: x[1], reverse = True)  # highest possible value -> least constraining
    return [tup[0] for tup in to_be_sorted]

def find_most_constrained_blank(state):
    curr_min = 10
    blank_with_curr_min = []

    for i in range(9):
        for j in range(9):
            curr_position = (i, j)
            if state[i][j] != 0:
                continue

            possible_dom_val = len(calculate_domain(state, curr_position))
            if possible_dom_val < curr_min:
                curr_min = possible_dom_val
                blank_with_curr_min = [curr_position]
            elif possible_dom_val == curr_min:
                blank_with_curr_min.append(curr_position)
            else:
                pass  # if higher possible_dom_val, not most constrained

    return blank_with_curr_min[0]

def find_next_empty_blank(state):
    for i in range(9):
        for j in range(9):
            if state[i][j] == 0:
                return (i, j)
    return False

def is_complete(state):
    for i in range(9):
        for j in range(9):
            if state[i][j] == 0:
                return False
    return True

def forward_checking(state):
    for i in range(9):
        for j in range(9):
            curr_position = (i, j)
            if state[i][j] != 0:
                continue

            possible_dom_val = len(calculate_domain(state, curr_position))
            if possible_dom_val == 0:
                return False
    return True

def revise(arc, domain, neighbour_domain):
    revised = False
    first = arc[0]
    second = arc[1]
    revised_variable_values = copy.deepcopy(domain)
    for value in domain:
        if len(neighbour_domain) == 1 and (value in neighbour_domain):
            revised_variable_values.remove(value)
            revised = True
    domain = revised_variable_values
    return revised

def AC3(new_state, x, y):
    current_pos = convert_81(x, y)
    queue = deque()
    neighbours = generate_neighbours(x, y) #huge overhead <- try to reduce
    
    possible_values = []
    for i in range(81):
        possible_values.append(set())
    possible_values[current_pos] = calculate_domain(new_state, [x,y])
    for neighbour in neighbours[current_pos]:
        possible_values[neighbour] = calculate_domain(new_state, [neighbour // 9, neighbour % 9])

    for neighbour in neighbours[current_pos]:
        queue.append([current_pos, neighbour])
        #queue.append([neighbour, current_pos])

    while len(queue) != 0:
        arc = queue.popleft()
        first = arc[0]
        second = arc[1] 
        #print str(second) + "tis is jolly neighbour"
        if revise(arc, possible_values[first], possible_values[second]):
            if len(possible_values) == 0:
                return False
            for neighbour in neighbours[first]:
                if neighbour != second:
                     queue.append([neighbour, current_pos])
    return True


def backtrack(state, count = 0):
    count += 1
    result = state
    if is_complete(state):
        return result

    #var_selected = find_most_constrained_blank(state)
    var_selected = find_next_empty_blank(state)
    domain = calculate_domain(state, var_selected)
    #sorted_domain = sort_by_least_constrained_value(state, domain, var_selected)
    for val in domain: 
        # val will be consistent since calculate_domain removes inconsistent value
        new_state = copy.deepcopy(state)
        x = var_selected[0]
        y = var_selected[1]
        new_state[x][y] = val
        if count > 0:
            if AC3(new_state, x, y):
            #if forward_checking(new_state):
                result = backtrack(new_state, count)
                if result:
                    #print str(count)
                    return result
        else:
            result = backtrack(new_state, count)
            if result:
                #print str(count)
                return result
    return False  # sudoku instance is always solvable

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    def solve(self):
        start = time.time()
        result = backtrack(self.ans)
        end = time.time()
        print str(end - start)
        # self.ans is a list of lists
        return result

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")

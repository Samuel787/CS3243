import sys, copy, time

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

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

def backtrack(state, totalBacktracks = 0, depth = 0, maxDepth = 0):
    depth += 1
    if maxDepth < depth:
        maxDepth = depth
    totalBacktracks += 1

    result = state
    if is_complete(state):
        return result, totalBacktracks, depth, maxDepth

    var_selected = find_most_constrained_blank(state)
    domain = calculate_domain(state, var_selected)
    #sorted_domain = sort_by_least_constrained_value(state, domain, var_selected)
    for val in domain: 
        # val will be consistent since calculate_domain removes inconsistent value
        new_state = copy.deepcopy(state)
        x = var_selected[0]
        y = var_selected[1]
        new_state[x][y] = val

        # forward checking here
        if forward_checking(new_state):
            result, totalBacktracks, depth, maxDepth = backtrack(new_state, totalBacktracks, depth, maxDepth)
            if result:
                return result, totalBacktracks, depth, maxDepth 
        depth -= 1
    return False, totalBacktracks, depth, maxDepth  # sudoku instance is always solvable


class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists
        self.timeTaken = 0 # self.timeTaken is the time taken to run the algorithm
        self.totalBacktracks = 0 # self.totalBacktracks is the number of backtracks (time efficiency metric)
        self.depth = 0 # self.depth is the current depth of the backtracking algorithm at any given instance (space complexity metric)
        self.maxDepth = 0 # self.maxDepth is the maximum depth reached by the backtracking algorithm in all instances (space complexity metric)

    def solve(self):
        # self.ans is a list of lists

        # print 'backtrack '+str(self.totalBacktracks)
        # print 'maxDepth '+str(self.maxDepth)
        start = time.time()
        result,self.totalBacktracks,self.depth,self.maxDepth = backtrack(self.ans)
        self.timeTaken = time.time() - start
        # print 'time taken '+str(self.timeTaken)
        # print 'backtrack '+str(self.totalBacktracks)
        # print 'maxDepth '+str(self.maxDepth)

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
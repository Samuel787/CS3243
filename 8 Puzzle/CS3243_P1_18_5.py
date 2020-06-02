import os, time, sys
import CS3243_P1_18_1 as BFS
import CS3243_P1_18_2 as MisplacedTiles
import CS3243_P1_18_3 as Manhattan
import CS3243_P1_18_4 as Manhattan_Linear

if __name__ == "__main__":
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

    timeEfficiency = []
    nodeEfficiency = []

    # BFS algorithm 
    index0 = "BFS"
    puzzle0 = BFS.Puzzle(init_state, goal_state)
    puzzle0.solve()
    if (puzzle0.nodes_expanded != 0):
        timeEfficiency.append([index0, puzzle0.time_taken])
        nodeEfficiency.append([index0, puzzle0.nodes_expanded])

    # A*Star algorithm with Manhattan distance heuristic 
    index1 = "Manhattan Distance Heuristic"
    puzzle1 = Manhattan.Puzzle(init_state, goal_state)
    puzzle1.solve()
    if (puzzle1.nodes_expanded != 0):
        timeEfficiency.append([index1, puzzle1.time_taken])
        nodeEfficiency.append([index1, puzzle1.nodes_expanded])

    # A*Star algorithm with Manhattan distance with linear conflicts heuristic 
    index2 = "Manhattan Distance with Linear Conflicts Heuristic"
    puzzle2 = Manhattan_Linear.Puzzle(init_state, goal_state)
    puzzle2.solve()
    if (puzzle2.nodes_expanded != 0):
        timeEfficiency.append([index2, puzzle2.time_taken])
        nodeEfficiency.append([index2, puzzle2.nodes_expanded])

    # A*Star algorithm with Misplaced Tiles heuristic 
    index3 = "Misplaced Tiles Heuristic"
    puzzle3 = MisplacedTiles.Puzzle(init_state, goal_state)
    puzzle3.solve()
    if (puzzle3.nodes_expanded != 0):
        timeEfficiency.append([index3, puzzle3.time_taken])
        nodeEfficiency.append([index3, puzzle3.nodes_expanded])

    print("")
    if timeEfficiency == [] or nodeEfficiency == []:
        print("Given input is unsolvable")
    else:
        timeEfficiency.sort(key=lambda tup: tup[1])
        print("Algorithms in order of Time Efficiency:")
        for i in timeEfficiency:
            print(str(round(i[1],2))+" seconds:", i[0])
        print("")
        nodeEfficiency.sort(key=lambda tup: tup[1])
        print("Algorithms in order of Nodes Expanded:")
        for i in nodeEfficiency:
            print(str(i[1])+" nodes:", i[0])

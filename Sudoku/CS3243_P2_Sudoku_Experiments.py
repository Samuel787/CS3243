import sys, copy, time
import CS3243_P2_Sudoku_AC3_Samuel_Copy as AC3
import CS3243_P2_Sudoku_Fwd_Checking_Ronald_Copy as FC

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

    timeTaken = []
    totalBacktracks = []
    maxDepth = []

    # AC3 algorithm 
    index0 = "AC3"
    AC3_sudoku = AC3.Sudoku(puzzle)
    AC3_sudoku.solve()
    timeTaken.append([index0, AC3_sudoku.timeTaken])
    totalBacktracks.append([index0, AC3_sudoku.totalBacktracks])
    maxDepth.append([index0, AC3_sudoku.maxDepth])

    # Forward Checking algorithm 
    index1 = "Forward Checking"
    FC_sudoku = FC.Sudoku(puzzle)
    FC_sudoku.solve()
    timeTaken.append([index1, FC_sudoku.timeTaken])
    totalBacktracks.append([index1, FC_sudoku.totalBacktracks])
    maxDepth.append([index1, FC_sudoku.maxDepth])

    if timeTaken == [] or maxDepth == []:
        print("Given input is unsolvable")
    else:
        timeTaken.sort(key=lambda tup: tup[1])
        print("Algorithms in order of Time Efficiency:")
        for i in timeTaken:
            print str(round(i[1],2))+" seconds: " + str(i[0])
        print("")
        totalBacktracks.sort(key=lambda tup: tup[1])
        print("Algorithms in order of total backtracks:")
        for i in totalBacktracks:
            print str(i[1])+" total backtracks: " + str(i[0])
        print("")
        maxDepth.sort(key=lambda tup: tup[1])
        print("Algorithms in order of max depth:")
        for i in maxDepth:
            print str(i[1])+" max depth: " + str(i[0])

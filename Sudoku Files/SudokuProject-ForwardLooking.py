with open("puzzles_6_variety_hard.txt") as f:
    puzzles = [line.strip()for line in f]
for amountOfPuzzles in range(len(puzzles)):
    tempPuzzle = puzzles[amountOfPuzzles]

    length = len(tempPuzzle)
    n = int(length**0.5)

    sub_height = int(n**0.5)
    while n%sub_height != 0:
        sub_height -=1
    sub_width = n//sub_height

    #print(length, sub_height, sub_width)
    symbols = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:n]

    constraintSet = []
    #length
    temp_list = []
    for i in range(len(tempPuzzle)):
        if(i < n):
            temp_list.append(i)
            constraintSet.append(temp_list)
            temp_list = []
        else:
            constraintSet[i%n].append(i)
    #print(constraintSet)

    #width
    temp_list = []
    for i in range(len(tempPuzzle)):
        if(i%n == 0 and i != 0):
            constraintSet.append(temp_list)
            temp_list = []
        temp_list.append(i)
    constraintSet.append(temp_list)
    #print(constraintSet)

    #little boxes :(
    for sub_row in range(sub_width):
        for sub_column in range(sub_height):
            row = sub_row * sub_height
            column = sub_column * sub_width
            temp_list = []
            for row_count in range(sub_height):
                for column_count in range(sub_width):
                    current_r = row + row_count
                    current_c = column + column_count
                    i = current_r * n +current_c
                    temp_list.append(i)
            constraintSet.append(temp_list)
    #print(constraintSet)
    neighborDict = {}
    for symbol in range(len(tempPuzzle)):
        neighborDict[symbol] = set()
        for lists in constraintSet:
            if(symbol in lists):
                new_set = set(lists)
                new_set.remove(symbol)
                for i in new_set:
                    neighborDict[symbol].add(i)
    def goal_test(puzzle):
        for i in puzzle:
            if(len(puzzle[i]) > 1):
                return False
        return True
    #print(neighborDict[1])
    def get_next_unassigned_var(puzzle):
        smallestInt = 100
        for i in range(len(puzzle)):
            if(len(puzzle[i]) < smallestInt and len(puzzle[i]) > 1):
                smallestInt= len(puzzle[i])
                smallestIndex = i
        return smallestIndex
            
    # def get_sorted_values(puzzle, spot):
    #     newSymbols = set(symbols)
    #     occupiedSpots = set()
    #     for list in neighborDict[spot]:
    #         for i in list:
    #             occupiedSpots.add(puzzle[i])
    #     iterationSet = set(newSymbols)
    #     for symbol in iterationSet:
    #         #print(len(iterationSet))
    #         if(symbol in occupiedSpots):
    #             newSymbols.remove(symbol)
    #     return newSymbols
    
    def f_l(board, solvedCellList):
        for index in solvedCellList:
            val = list(board[index])[0]
            for neighbor_index in neighborDict[index]:
                if(val in board[neighbor_index]):
                    board[neighbor_index].remove(val)
                    if(len(board[neighbor_index]) == 1):
                        solvedCellList.append(neighbor_index)
                    if(len(board[neighbor_index]) == 0):
                        return None
        return board
    def constraint_p(board):
        solvedCells = []
        for symbol in symbols:
            for constraintList in constraintSet:
                symbolIndex = -1
                for index in constraintList:
                    if(symbol in board[index]):
                        if(len(board[index]) == 1):
                            symbolIndex = -1
                            break
                        if(symbolIndex == -1):
                            symbolIndex = index
                        else:
                            symbolIndex = -1
                            break
                if(symbolIndex != -1):
                    solvedCells.append(symbolIndex)
                    _board = board[symbolIndex].copy()
                    for val in _board:
                        if(val != symbol):
                            board[symbolIndex].remove(val)
        return board, solvedCells
#for every val 
#for every contraint set
#if a value only appears once in an unsolved cell/spot (len of set is greater than 1)
#solve that cell
#keep list of all cells solved by contraint propagation
    
  #add next checked state for constrait propagation
    #keep list of all cells solved by contraint propagation
    board = {x:set(symbols) for x in range(length)}
    solvedCellList = []
    for i in range(length):
        if(tempPuzzle[i] != "."):
            board[i] = set(tempPuzzle[i])
            solvedCellList.append(i)
    #print(solvedCellList)
    returnedBoard = f_l(board, solvedCellList)

    
    def csp_backtracking(puzzle):
        if(goal_test(puzzle)):
            return puzzle
        spot = get_next_unassigned_var(puzzle)
        #print(state)
        for val in sorted(puzzle[spot]):
            new_state = {x:puzzle[x].copy() for x in puzzle}
            new_state[spot] = set(val)
            checked_state = f_l(new_state, [spot])
            if(checked_state is not None):
                checked_state_2, solvedCells = constraint_p(checked_state)
                #print(checked_state_2)
                if(checked_state_2 is not None):
                    checked_state_3 = f_l(checked_state_2, solvedCells)
                    if(checked_state_3 is not None):
                        result = csp_backtracking(checked_state_3)
                        if result is not None:
                            return result
        return None
    print("")
    print(amountOfPuzzles)
    solution = csp_backtracking(returnedBoard)  
    str1 = ""
    for i in solution:
        str1 += list(solution[i])[0]
    #print(solution)
    print(str1)
    print("")
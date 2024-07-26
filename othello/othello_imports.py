board = "xxoo.xox.....oox......oxo..ooxooo..oox.ox.xxx..oxoox...o.....xox"
#01234567
#89101112131415
def convert_to_10x10(board):
    newBoard = "?????????"
    r = 8
    for i in range(len(board)):
        if(i%r == 0):
            newBoard += "??"
        newBoard += board[i]
    newBoard += "???????????"
    return newBoard
def PrintBoard(board, row):
    str1 = ""
    for i in range(len(board)):
        if(i%row ==0):
            #print(str1)
            str1 =""
        str1 += board[i]
    #print(str1)

def possible_moves(board, token):
    newBoard = convert_to_10x10(board)
    opponent = "o"
    if(token == "o"):
        opponent = "x"
    directionList = [-11, -10, -9, -1, 1, 9, 10, 11]
    avalaibleMoves= []
    for index in range(100):
        if(newBoard[index] == token):
            for direction in directionList:
                if(newBoard[index + direction] == opponent):
                    checkingIndex = index + direction
                    while(newBoard[checkingIndex] == opponent):
                        checkingIndex += direction
                    if(newBoard[checkingIndex] == "."):
                        newMove = convert_to_8x8(checkingIndex)
                        #print(newMove)
                        if(newMove not in avalaibleMoves):
                            avalaibleMoves.append(newMove)
    #print(avalaibleMoves)
    return avalaibleMoves
def make_move(board, token, index):
    opponentToken = "x"
    if(opponentToken == token):
        opponentToken = "o"
    
    newBoard = list(board)
    newBoard[index] = "F"
    newBoardTen = convert_to_10x10(''.join(newBoard))
    #PrintBoard(newBoardTen, 10)
    tenIndex = newBoardTen.index("F")
    newBoard[index] = token
    directionList = [-11, -10, -9, -1, 1, 9, 10, 11]
    for direction in directionList:
        indexsToFlip = []
        checkingIndex = 0
        #print(tenIndex+ direction)
        if(newBoardTen[tenIndex + direction] == opponentToken):
            checkingIndex = tenIndex + direction
            indexsToFlip.append(checkingIndex)
            while(newBoardTen[checkingIndex] == opponentToken):
                checkingIndex += direction
                indexsToFlip.append(checkingIndex)
            if(newBoardTen[checkingIndex] == token):
                #print(indexsToFlip)
                for i in indexsToFlip:
                    newBoard[convert_to_8x8(i)] = token;
    return "".join(newBoard)

def convert_to_8x8(index):
    r = index//10
    c = index%10
    #print((r*10)+c)
    r-=1
    c-=1
    newIndex = (r*8)+c
    return newIndex

#convert avalaible move indicies back to 8x8 indicies as they are indicies in 10x10 board

#take index of possible move and convert it to a row and column, then subtract by r and c by 1 because its up one and one to the left without ? marks then just
#multiply new r and c

#PrintBoard(convert_to_10x10(board), 10)
#print(possible_moves(board, "o"))
moves = possible_moves(board, "o")
newMoves = []
for i in moves:
    newMoves.append(convert_to_8x8(i))

#PrintBoard(board, 8)
newBoard = list(board)
for i in range(len(newBoard)):
    if(i in newMoves):
        newBoard[i] = "O"
PrintBoard(board, 8)
PrintBoard(make_move(board, "o", 4), 8)
#PrintBoard("".join(newBoard), 8)
#print(newMoves)


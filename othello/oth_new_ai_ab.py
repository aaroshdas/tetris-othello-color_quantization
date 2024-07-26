from othello_imports import possible_moves, make_move
import sys

board = sys.argv[1]
player = sys.argv[2]

# board = "xxoo.xox.....oox......oxo..ooxooo..oox.ox.xxx..oxoox...o.....xox"
# player = "x"
#beat oth_corners_unpredicitable all the time

#alpha is biggest num so starts -100000 in max node we update alpha
#beta is smallest

def find_next_move(board, player, depth):
    if(player == "x"):
            newMoves = possible_moves(board, player)
            highestScore = -100000000000000
            bestMove = 0
            for i in newMoves:
                newScore = min_step(make_move(board, player, i), depth, -100000, 100000)
                if(newScore > highestScore):
                    highestScore = newScore
                    bestMove = i
            return bestMove
    else:
        newMoves = possible_moves(board, player)
        lowestScore = 100000000000000
        bestMove = 0
        for i in newMoves:
            newScore = max_step(make_move(board, player, i), depth, -100000, 100000)
            if(newScore < lowestScore):
                lowestScore = newScore
                bestMove = i
        return bestMove
#pos better for x ++
#neg better for o --
    
# uses O -
def min_step(board, depth, alpha, beta):
    newMoves = possible_moves(board, "o")
    bestVal = 100000000
    if(len(newMoves) == 0 and len(possible_moves(board, "x")) == 0):
        if(board.count("o") > board.count("x")):
            return -1000000
        elif(board.count("o") < board.count("x")):
            return 1000000
        else:
            return 0
    if(depth == 0):
        return score(board)
    if(len(newMoves) == 0):
        return max_step(board, depth, alpha, beta)
    for i in newMoves:
        val = max_step(make_move(board, "o", i), depth-1, alpha, beta)
        if(val <= beta):
            beta = val
            if(alpha >= beta):
                return val
        if(val < bestVal):
            bestVal = val
    return bestVal
        

# uses X +
def max_step(board, depth, alpha, beta):
    newMoves = possible_moves(board, "x")
    bestVal = -100000000
    if(len(newMoves) == 0 and len(possible_moves(board, "x")) == 0):
        if(board.count("o") > board.count("x")):
            return -1000000
        elif(board.count("o") < board.count("x")):
            return 1000000
        else:
            return 0
    if(depth == 0):
        return score(board)
    if(len(newMoves) == 0):
        return min_step(board, depth, alpha, beta)
    for i in newMoves:
        val = min_step(make_move(board, "x", i), depth-1, alpha, beta)
        if(val >= alpha):
            alpha = val
            if(alpha >= beta):
                return val
        if(val > bestVal):
            bestVal = val
    return bestVal

corners = [0, 7, 55, 63]
nearCorners = {0:[1,8,9], 7:[6,14,15], 56:[48,49,57], 63:[54,55,62]}
def score(board):
    score = 0
    score =  len(possible_moves(board, "x"))-len(possible_moves(board, "o"))
    cornerCoefficient = 25
    nearCornerCoefficient = 15
    for i in corners:
        if(board[i] == "x"):
            score += cornerCoefficient
        if(board[i] =="o"):
            score -= cornerCoefficient
    for k in nearCorners:
        if(board[k] == "."):
            for h in nearCorners[k]:
                if(h == "x"):
                    score -= nearCornerCoefficient
                if(h == "o"):
                    score += nearCornerCoefficient
    
    endgamePieceCoefficient = 100
    if(board.count(".") <= 7):
        score += (board.count("x") - board.count("o"))*endgamePieceCoefficient
    
    return score
    

depth = 1
for count in range(board.count(".")):  # Max num of possible future moves
   print(find_next_move(board, player, depth))
   depth += 1
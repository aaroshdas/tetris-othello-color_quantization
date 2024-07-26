from othello_imports import possible_moves, make_move
import sys

corners = {
    0: {1, 8, 9},
    7: {6, 14, 15},
    56: {57, 48, 49},
    63: {62, 54, 55}
}

def score(board, token, enemy, done=False):
    if done:
        me = board.count(token)
        them = board.count(enemy)
        if me > them:
            return 1000 + (me - them)
        elif them > me:
            return -1000 + (me - them)
        else:
            return 0
    movement = len(possible_moves(board, token)) - len(possible_moves(board, enemy))
    for corner in corners:
        if board[corner] == token:
            movement += 100
            for loc in corners[corner]:
                if board[loc] == token:
                    movement += 10
        elif board[corner] == enemy:
            movement -= 100
            for loc in corners[corner]:
                if board[loc] == enemy:
                    movement -= 10
        else:
            for loc in corners[corner]:
                if board[loc] == token:
                    movement -= 10
                elif board[loc] == enemy:
                    movement += 10
    return movement


def negamax(board, token, enemy, alpha, beta, depth):
    moves = possible_moves(board, token)
    if len(moves) == 0:
        other_moves = possible_moves(board, enemy)
        if len(other_moves) > 0:
            if depth > 0:
                return -1 * negamax(board, enemy, token, -1 * beta, -1 * alpha, depth-1)
            else:
                return score(board, token, enemy)
        else:
            return score(board, token, enemy, True)
    if depth == 0:
        return score(board, token, enemy)
    ret_max = -1 * 10**10
    for poss_move in possible_moves(board, token):
        new_board = make_move(board, token, poss_move)
        future = -1 * negamax(new_board, enemy, token, -1 * beta, -1 * alpha, depth-1)
        if future > ret_max:
            ret_max = future
            if ret_max > alpha:
                alpha = ret_max
                if alpha >= beta:
                    return ret_max
    return ret_max


def find_next_move(board, token, depth):
    enemy = "xo"["ox".index(token)]
    poss = possible_moves(board, token)
    boards = [(index, make_move(board, token, index)) for index in poss]
    best = -1 * 10 ** 10
    alpha = -1 * 10 ** 10
    beta = 10 ** 10
    temp_best = -1
    for index, new_board in boards:
        new_val = -1 * negamax(new_board, enemy, token, -1 * beta, -1 * alpha, depth - 1)
        if new_val > best:
            best = new_val
            temp_best = index
    return temp_best



board = sys.argv[1]
player = sys.argv[2]
depth = 1
for count in range(board.count(".")):  # 15 is arbitrary; a depth that your code won't reach, but infinite loops crash the grader
   print(find_next_move(board, player, depth))
   depth += 1
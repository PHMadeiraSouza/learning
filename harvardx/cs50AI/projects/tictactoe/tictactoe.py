"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    omoves = 0
    xmoves = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                xmoves += 1
            elif board[i][j] == O:
                omoves += 1

    if xmoves <= omoves:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possiblemoves = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possiblemoves.add((i,j))
    return possiblemoves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newboard = deepcopy(board)
    try:
        if newboard[action[0]][action[1]] == EMPTY:
            newboard[action[0]][action[1]] = player(newboard)
            return newboard
    except:
        raise Exception('ilegal move')


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
    for j in range(3):    
        if board[0][j] == board[1][j] == board[2][j]:
            return board[0][j]
        
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) == None:
        if any(EMPTY in sublist for sublist in board):
            return False
        else:
            return True
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        v = -math.inf
        for action in actions(board):
            minmove = max(v, Min_Value(result(board, action)))
            if minmove > v:
                v = minmove
                bestmove = action
    else:
        v = math.inf
        for action in actions(board):
            maxmove = min(v, Max_Value(result(board, action)))
            if maxmove < v:
                v = maxmove
                bestmove = action

    return bestmove
    
            
def Max_Value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        maxvalue = max(v, Min_Value(result(board, action)))
        if maxvalue > v:
            v = maxvalue
    return v

def Min_Value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        minvalue = min(v, Max_Value(result(board, action)))
        if minvalue < v:
            v = minvalue
    return v

"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None

negative_inf = float('-inf')

DEBUG = 1
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
    if DEBUG:
        print("in player")
    # count X and O
    x_count = 0
    o_count = 0
    for row in board:
        for col in row:
            if col == X:
                x_count += 1
            if col == O:
                o_count += 1
    if x_count >= o_count:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if DEBUG:
        print("in actions")
    actions = []
    for row_idx in range(3):
        for col_idx in range(3):
            if board[row_idx][col_idx] == EMPTY:
                actions.append((row_idx, col_idx))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if DEBUG:
        print("in result")
    whose_turn = player(board)
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = whose_turn
    return new_board


def if_player_win(board, player):
    """
    Return if the given player has won or not on the board
    """
    if DEBUG:
        print("in won_or_no")
    # hor
    for row in board:
        if (row[0] == player) and (row[1] == player) and (row[2] == player):
            return True
    # ver
    for col_idx in range(3):
        memo = True
        for row_idx in range(3):
            memo = memo and (board[row_idx][col_idx] == player)
        if memo:
            return player
    # dia
    # first diagonal
    memo = True
    for idx in range(3):
        memo = memo and (board[idx][idx] == player)
    if memo:
        return player
    # (0,0) (1,1) (2,2)
    # (0,2) (1,1) (2,0)
    # second diagonal
    memo = True
    for i in range(3):
        for j in range(2, -1, -1):
            memo = memo and (board[i][j] == player)
    if memo:
        return player
    return False


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if DEBUG:
        print("in winner")
    if if_player_win(board, X):
        return X
    if if_player_win(board, O):
        return O
    return None


def is_filled(board):
    if DEBUG:
        print("in is_filled")
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                return False
    return True


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if DEBUG:
        print("in terminal")
    return winner(board) is not None or is_filled(board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if DEBUG:
        print("in utility")
    winner_ = winner(board)
    if winner_ == X:
        return 1
    elif winner_ == O:
        return -1
    else:
        return 0


def min_value(board):
    """try to minimise the score of the board"""
    if DEBUG:
        print("in min_value")
    v = float('inf')
    optimal_action = None
    if terminal(board):
        return utility(board), optimal_action
    actions_ = actions(board)
    for action in actions_:
        v = min(v, max_value(result(board, action))[0])
        if (max_value(result(board, action)))[0] < v:
            optimal_action = action
    return v, optimal_action


def max_value(board):
    """try to maximise the score of the board"""
    if DEBUG:
        print("in max_value")
    v = negative_inf
    optimal_action = None
    if terminal(board):
        return utility(board), optimal_action
    actions_ = actions(board)
    for action in actions_:
        v = max(v, min_value(result(board, action))[0])
        if (min_value(result(board, action)))[0] > v:
            optimal_action = action
    return v, optimal_action

    

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    X tries to maximise. O tries to minimise
    """
    if DEBUG:
        print("in minimax")
    if terminal(board):
        return None
    player_ = player(board)
    if player_ == X:
        return max_value(board)[1]
    return min_value(board)[1]
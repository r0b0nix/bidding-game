"""
An AI agent for land bidding process.
"""
import math
import random
import sys
import time

# You can use the functions in utilities to write your AI
from typing import Dict, Any

from utilities import find_lines, get_possible_moves, get_score, play_move


def eprint(*args, **kwargs):  # you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)


# Method to compute utility value of terminal state
# which we define to be the
# number of hectares they own minus the number of hectares their competitor owns
def compute_utility(board, color):
    n1, n2 = get_score(board)
    if color == 1:
        return n1 - n2
    else:
        return n2 - n1

# Compute the utility value of a move.
def move_utility (board, color, move):
    result = play_move(board, color, move[0], move[1])
    value = compute_utility(result, color)
    return value

# Better heuristic value of board
def compute_heuristic(board, color):  # not implemented, optional
    # IMPLEMENT
    return 0  # change this!


def mm_min_node_1(board, color, limit, caching=0):
    value = -math.inf
    for move in get_possible_moves(board, color):
        dim = range(len(board))
        child = play_move(board, color, dim, dim)
        v = mm_min_node(child, color, limit - 1)
        value = min(value, v)
        return move, value


############ MINIMAX ###############################
def mm_min_node(board, color, limit, caching=0):
    v = []
    moves = {}
    index = 0
    for move in get_possible_moves(board, color):
        gain = move_utility(board, color, move)
        v.append(gain)
        moves[index] = move
        index += 1
    low = v.index(min(v))
    return moves[low], min(v)  # The best move and its value.


def get_move_count(board, color):
    return len(get_possible_moves(board, color))


def terminal_state(board, color):
    if get_move_count (board, color) == 0:
        return True
    else:
        return False


def mm_max_node_2(board, color, limit, caching=0):
    num_moves = get_move_count(board, color)
    if num_moves == 1:  # last move, recursion stopping condition
        last_move = get_possible_moves(board, color)
        value = move_utility(board, color, last_move)
        return last_move, value
    #  Otherwise, to recurse is divine
    v = -math.inf
    for move in get_possible_moves(board, color):
        result = play_move(board, color, move[0], move[1])
        best_move, r_val = mm_max_node(result, color, limit - 1, caching)
        v = max(v, r_val)
    return best_move, v


def mm_max_node(board, color, limit, caching=0):
    v = []
    moves = {}
    index = 0
    for move in get_possible_moves(board, color):
        gain = move_utility(board, color, move)
        v.append(gain)
        moves[index] = move
        index += 1
    best = v.index(max(v))
    return moves[best], max(v)  # The best move and its value.


def claim_mm(board, color, limit, caching=0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    """
    if color == 1:  # assuming your turn (maximizing player)
        plot, value = mm_max_node(board, color, limit)
    else:  # The other player
        plot, value = mm_min_node(board, color, limit)
    return plot


############ ALPHA-BETA PRUNING #####################

def ab_min_node(board, color, alpha, beta, limit, caching=0, ordering=0):
    v = []
    moves = {}
    index = 0
    for move in get_possible_moves(board, color):
        gain = move_utility(board, color, move)
        v.append(gain)
        moves[index] = move
        index += 1
    low = v.index(min(v))
    return moves[low], min(v)  # The best move and its value.


def ab_max_node(board, color, alpha, beta, limit, caching=0, ordering=0):
    v = []
    moves = {}
    index = 0
    for move in get_possible_moves(board, color):
        gain = move_utility(board, color, move)
        v.append(gain)
        moves[index] = move
        index += 1
    best = v.index(max(v))
    return moves[best], max(v)  # The best move and its value.


def claim_ab(board, color, limit, caching=0, ordering=0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations.
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations.
    """
    alpha = 1
    beta = 1
    if color == 1:  # assuming your turn (maximizing player)
        plot, value = ab_max_node(board, color,alpha, beta,  limit)
    else:  # The other player
        plot, value = ab_min_node(board, color,alpha, beta,  limit)
    return plot


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Bidding AI")  # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0])  # Player color: 1 for dark (goes first), 2 for light.
    limit = int(arguments[1])  # Depth limit
    minimax = int(arguments[2])  # Minimax or alpha beta
    caching = int(arguments[3])  # Caching
    ordering = int(arguments[4])  # Node-ordering (for alpha-beta only)

    if (minimax == 1):
        eprint("Running MINIMAX")
    else:
        eprint("Running ALPHA-BETA")

    if (caching == 1):
        eprint("State Caching is ON")
    else:
        eprint("State Caching is OFF")

    if (ordering == 1):
        eprint("Node Ordering is ON")
    else:
        eprint("Node Ordering is OFF")

    if (limit == -1):
        eprint("Depth Limit is OFF")
    else:
        eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL":  # Game is over.
            print
        else:

            board = eval(input())  # Read in the input and turn it into a Python
            # object. The format is a list of rows. The
            # squares in each row are represented by
            # 0 : empty square
            # 1 : dark disk (player 1)
            # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1):  # run this if the minimax flag is given
                movei, movej = claim_mm(board, color, limit, caching)
            else:  # else run alphabeta
                movei, movej = claim_ab(board, color, limit, caching, ordering)

            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()

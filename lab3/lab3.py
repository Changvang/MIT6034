# 6.034 Fall 2010 Lab 3: Games
# Name: D:\Program\Github\MIT6034\lab3
# Email: <Your Email>

from util import INFINITY

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 3

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 2

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
##
## Uncomment this line to play a game as white:
#run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
#run_game(basic_player, human_player)

## Or watch the computer play against itself:
#run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """
    #It likely basic_evaluate
    if board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        score = -1000
    else:
        #print board.chain_cells(board.get_current_player_id())
        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefer having your pieces in the center of the board.
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)
    #print score
    return score


## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,eval_fn=focused_evaluate)

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.

#It run ok with test but can use to play like a player .
 ########## And i don't know why so I try create another alpha_bata_player


# def toplevel_bestvalue_alpha_beta(board, depth , eval_fn, get_next_moves_fn , is_terminal_fn , alpha, beta):
#     ##This have contructure from max_value_alpha_beta but only get best move
#     Bestmove = -1
#     val = NEG_INFINITY
#     for move , new_board in get_next_moves_fn(board):
#         Min_val = min_value_alpha_beta(new_board, depth -1, eval_fn, get_next_moves_fn, is_terminal_fn, alpha, beta)
#         print(Min_val)
#         if ( Min_val > val):
#             Bestmove = move
#             val = Min_val
#         alpha = max(alpha, val)
#         if alpha >= beta:
#             return move
#     return Bestmove
#
#
# def max_value_alpha_beta(board, depth , eval_fn, get_next_moves_fn , is_terminal_fn , alpha, beta):
#     if is_terminal_fn(depth, board):
#         return eval_fn(board)
#     val = NEG_INFINITY;
#     for move , new_board in get_next_moves_fn(board):
#         val = max(val, min_value_alpha_beta(new_board, depth -1, eval_fn, get_next_moves_fn, is_terminal_fn, alpha, beta))
#         alpha = max(alpha, val)
#         if alpha >= beta:
#             return alpha
#     print val
#     return val
#
# def min_value_alpha_beta(board, depth , eval_fn, get_next_moves_fn , is_terminal_fn , alpha, beta):
#     if is_terminal_fn(depth, board):
#         return -eval_fn(board)
#     val = INFINITY;
#     for move, new_board in get_next_moves_fn(board):
#         val = min(val, max_value_alpha_beta(new_board, depth -1, eval_fn, get_next_moves_fn, is_terminal_fn, alpha, beta) )
#         beta = min(beta, val)
#         if alpha >= beta:
#             return beta
#     print val
#     return val


def toplevel_bestvalue_alpha_beta(board, depth , eval_fn, get_next_moves_fn , is_terminal_fn , alpha , beta):
    # It only using maximum
    if is_terminal_fn(depth,  board):
        return eval_fn(board), None

    val  = NEG_INFINITY;
    best_move = -1

    for move, new_board in get_next_moves_fn(board):
        #replace alpha and beta
        new_alpha = -beta
        new_beta = -alpha
        #find value from layer and compare to get max val,move $ Val must get -Val?  $
        new_val = -1 * toplevel_bestvalue_alpha_beta(new_board, depth-1 , eval_fn, get_next_moves_fn , is_terminal_fn , new_alpha , new_beta)[0]
        #replace if have best_val
        if new_val > val:
            val, best_move = new_val, move
        #get new alpha if can
        alpha = max(alpha, val)
        #pruning if alpha >= beta
        if alpha >= beta:
            #print alpha
            return alpha, move
    #print val, best_move
    return val, best_move

def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
		      is_terminal_fn=is_terminal):
    return toplevel_bestvalue_alpha_beta(board, depth , eval_fn, get_next_moves_fn , is_terminal_fn , NEG_INFINITY, INFINITY)[1]

## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
alphabeta_player = lambda board: alpha_beta_search(board,
                                                   depth=8,
                                                   eval_fn=focused_evaluate)

## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)
#run_game(human_player, alphabeta_player)
#run_game(basic_player, alphabeta_player)
## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

def get_value_for_cell(board, row , col):
    if 0<= row <= 5 and 0<= col <= 6 :
        if board.get_cell(row,col) == board.get_other_player_id() :
            return 1
    return 0

def better_evaluate(board):
    if board.is_game_over():
        if board.is_win() == board.get_current_player_id():
            return 1000
        else:
            return -1000
    #board not over
    #print board.get_current_player_id()
    current_player_chain_cells = board.chain_cells(board.get_current_player_id())
    # fliter all chain 2 and 3 of Chain_set
    List_chain_with_more_2_continue = []
    for Chain in current_player_chain_cells:
        if len(Chain) >=2 :
            List_chain_with_more_2_continue.append(Chain)
    # Counting score = (4*chain_2 - end_cell) + (9*chain_3 - end_cell)+

    score = 0

    for Chain_set in List_chain_with_more_2_continue:
        # row chain
        if Chain_set[0][0] == Chain_set[1][0] :
            score += len(Chain_set)*3 - 2*( get_value_for_cell(board, Chain_set[0][0], Chain_set[0][1] + 1) + get_value_for_cell(board, Chain_set[0][0], Chain_set[len(Chain_set)-1][1] - 1))
        # col chain
        elif Chain_set[0][1] == Chain_set[1][1]:
            score += len(Chain_set)*3 - 2*(get_value_for_cell(board, Chain_set[0][0] + 1, Chain_set[0][1]) + get_value_for_cell(board, Chain_set[len(Chain_set) -1][0] - 1, Chain_set[0][1]))
        else:
            score += len(Chain_set)*3
            if Chain_set[0][0] + 1 == Chain_set[1][0]:
                if Chain_set[0][1] + 1 == Chain_set[1][1]:
                    score -= 2*(get_value_for_cell(board, Chain_set[0][0] - 1, Chain_set[0][1] - 1) + get_value_for_cell(board, Chain_set[len(Chain_set) -1][0] + 1, Chain_set[len(Chain_set)-1][1] + 1))
                if Chain_set[0][1] - 1 == Chain_set[1][1]:
                    score -= 2*(get_value_for_cell(board, Chain_set[0][0] - 1, Chain_set[0][1] + 1) + get_value_for_cell(board, Chain_set[len(Chain_set) -1][0] + 1, Chain_set[len(Chain_set)-1][1] - 1))
            if Chain_set[0][0] - 1 == Chain_set[1][0]:
                if Chain_set[0][1] + 1 == Chain_set[1][1]:
                    score -= 2*(get_value_for_cell(board, Chain_set[0][0] + 1, Chain_set[0][1] - 1) + get_value_for_cell(board, Chain_set[len(Chain_set) -1][0] - 1, Chain_set[len(Chain_set)-1][1] + 1))
                if Chain_set[0][1] - 1 == Chain_set[1][1]:
                    score -= 2*(get_value_for_cell(board, Chain_set[0][0] + 1, Chain_set[0][1] + 1) + get_value_for_cell(board, Chain_set[len(Chain_set) -1][0] - 1, Chain_set[len(Chain_set)-1][1] - 1))
        #print Chain_set, score
    # Prefer having your pieces in the center of the board.
    # for row in range(6):
    #     for col in range(7):
    #         if board.get_cell(row, col) == board.get_current_player_id():
    #             score -= abs(3-col)
    #         elif board.get_cell(row, col) == board.get_other_player_id():
    #             score += abs(3-col)
    return score

# Comment this line after you've fully implemented better_evaluate
#better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if False:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
    print "%s => %s" %(test_board_1, better_evaluate(test_board_1))

    # better evaluate from player 2
    print "%s => %s" %(test_board_2, better_evaluate(test_board_2))

## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

your_player = lambda board: alpha_beta_search(board, depth=4,
                                             eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
#run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
#run_game(your_player, basic_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])

def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)

## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = (False)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "1"
WHAT_I_FOUND_INTERESTING = "2"
WHAT_I_FOUND_BORING = "3"
NAME = "4"
EMAIL = "5"

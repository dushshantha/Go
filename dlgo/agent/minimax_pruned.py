import random
import enum

from dlgo.agent.base import Agent
from dlgo.agent.helpers import is_point_an_eye
from dlgo.goboard_slow import Move
from dlgo.gotypes import Point
from dlgo.gotypes import Player


MAX_SCORE = 999999
MIN_SCORE = -999999

class PrunedMiniaxAgent(Agent):

    def __init__(self, max_depth, eval_fn):
        Agent.__init__(self)
        self.max_depth = max_depth
        self.eval_fn = eval_fn

    def select_move(self, game_state):
        """
        Selects the next move using MiniMax
        :param game_state:
        :return:
        """
        best_moves = []
        best_score = None

        for possible_move in game_state.legal_moves():

            next_state = game_state.apply_move(possible_move)

            opponent_best_outcome = best_result(next_state, self.max_depth, self.eval_fn)
            our_best_outcome = -1 * opponent_best_outcome

            if (not best_moves) or our_best_outcome > best_score:
                best_moves = [possible_move]
                best_score = our_best_outcome

            elif our_best_outcome == best_score:
                best_moves.append(possible_move)

        return random.choice(best_moves)



def best_result(game_state, max_depth, eval_fn):
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return MAX_SCORE
        else:
            return MIN_SCORE

    if max_depth == 0:
        return eval_fn(game_state)

    best_result_so_far = MIN_SCORE
    for candidate_move in game_state.legal_moves():
        next_state = game_state.apply_move(candidate_move)
        opponent_best_result = best_result(next_state, max_depth - 1, eval_fn)
        our_result = -1 * opponent_best_result
        if our_result > best_result_so_far:
            best_result_so_far = our_result
    return best_result_so_far

def capture_diff(game_state):
    black_stones = 0
    white_stones = 0

    for r in range(1, game_state.board.num_rows + 1):
        for c in range(1, game_state.board.num_cols + 1):
            p = Point(r,c)
            color = game_state.board.get(p)
            if color == Player.black:
                black_stones += 1
            elif color == Player.white:
                white_stones += 1

    diff = black_stones - white_stones
    if game_state.next_player == Player.black:
        return diff
    return -1 * diff


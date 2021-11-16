#!/usr/bin/env python3
"""
Quoridor agent.
Copyright (C) 2013, <<<<<<<<<<< YOUR NAMES HERE >>>>>>>>>>>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""

from quoridor import *
import math


class MyAgent(Agent):

    """My Quoridor agent."""

    def play(self, percepts, player, step, time_left):
        """
        This function is used to play a move according
        to the percepts, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        :param percepts: dictionary representing the current board
            in a form that can be fed to `dict_to_board()` in quoridor.py.
        :param player: the player to control in this step (0 or 1)
        :param step: the current step number, starting from 1
        :param time_left: a float giving the number of seconds left from the time
            credit. If the game is not time-limited, time_left is None.
        :return: an action
          eg: ('P', 5, 2) to move your pawn to cell (5,2)
          eg: ('WH', 5, 2) to put a horizontal wall on corridor (5,2)
          for more details, see `Board.get_actions()` in quoridor.py
        """
        print("percept:", percepts)
        print("player:", player)
        print("step:", step)
        print("time left:", time_left if time_left else '+inf')
        
        # TODO: implement your agent and return an action for the current step.
        player_pos = percepts['pawns'][player]
        move = {'up':('P', player_pos[0]-1, player_pos[1]),
                'down':('P', player_pos[0]+1, player_pos[1]),
                'left':('P', player_pos[0], player_pos[1]-1),
                'right':('P', player_pos[0], player_pos[1]+1)}
        
        board = dict_to_board(percepts)
        # call apha-beta search
        _, move = h_alphabeta_search(board, player, 2, heuristic)
        print(move)
        return move
        # return move['left']
        # pass


def h_alphabeta_search(board, player, max_depth=6, h=lambda s , p: 0):
    """Search game to determine best action; use alpha-beta pruning.
    This version searches all the way to the leaves."""

    def max_value(board, alpha, beta, depth):
        # TODO: include a recursive call to min_value function
        # raise Exception("Function not implemented")
        if board.is_finished():
            return board.get_score(player), None
        
        if depth > max_depth:
            return h(board, player), None
        
        v, move = -math.inf, None
        for a in board.get_actions(player):
            transition = board.clone().play_action(a, player)
            v2, _ = min_value(transition, alpha, beta, depth+1)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def min_value(board, alpha, beta, depth):
        # TODO: include a recursive call to min_value function
        # raise Exception("Function not implemented")
        if board.is_finished():
            return board.get_score(1 - player), None
        if depth > max_depth:
            return h(board, 1 - player), None
        v, move = math.inf, None
        for a in board.get_actions(1 - player):
            transition = board.clone().play_action(a, 1 - player)
            v2, _ = max_value(transition, alpha, beta, depth+1)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    # print(max_depth)
    return max_value(board, -math.inf, math.inf, max_depth )

def cutoff_depth(d):
    """A cutoff function that searches to depth d."""
    return lambda board, depth: depth > d

def heuristic(board, player):
    score = board.get_score()
    print('Score:', score)
    sp = board.get_shortest_path(player)
    print('Shortest_path:', len(sp))
    if len(sp)==1:
        score+=1000
    return score


if __name__ == "__main__":
    agent_main(MyAgent())

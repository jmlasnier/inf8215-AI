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
        # print("percept:", percepts)
        # print("player:", player)
        # print("step:", step)
        # print("time left:", time_left if time_left else '+inf')
        
        # TODO: implement your agent and return an action for the current step.
        player_pos = percepts['pawns'][player]
        move = {'up':('P', player_pos[0]-1, player_pos[1]),
                'down':('P', player_pos[0]+1, player_pos[1]),
                'left':('P', player_pos[0], player_pos[1]-1),
                'right':('P', player_pos[0], player_pos[1]+1)}
        
        board = dict_to_board(percepts)
        # movelist = board.get_actions(player)
        
        shortestP = board.get_shortest_path(player)
        # print(shortestP)
        if len(shortestP) == 1:
            if player==0:
                return move['down']
            elif player==1:
                return move['up']
        # call apha-beta search
        # _, move = h_alphabeta_search(board, player, 2, heuristic)
        move = mcts(board, player, 5)
        print("move chosen :")
        print(move)
        return move
        # return move['left']
        # pass


def h_alphabeta_search(board : Board, player, max_depth=6, h=lambda s , p: 0):
    """Search game to determine best action; use alpha-beta pruning.
    This version searches all the way to the leaves."""

    def max_value(board : Board, alpha, beta, depth):
        # TODO: include a recursive call to min_value function
        # raise Exception("Function not implemented")
        print(f"max: depth {depth}")

        if board.is_finished():
            print(f"max: returning final get_score {board.get_score(player)}, {None}")
            return board.get_score(player), None
        
        if depth > max_depth:
            print(f"max: returning heuristic {h(board, player)}, {None}")
            return h(board, player), None
        
        v, move = -math.inf, None
        for a in board.get_actions(player):
            transition = board.clone().play_action(a, player)
            v2, _ = min_value(transition, alpha, beta, depth+1)
            print(f"max: min_value returned {v2}, {None}")
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                print(f"max: pruning and returning {v}, {move}")
                return v, move

        print(f"max: returning end of loop {v}, {move}")
        return v, move

    def min_value(board : Board, alpha, beta, depth):
        # TODO: include a recursive call to min_value function
        # raise Exception("Function not implemented")
        print(f"min: depth {depth}")

        if board.is_finished():
            print(f"min: returning final get_score {board.get_score(1 - player)}, {None}")
            return board.get_score(1 - player), None

        if depth > max_depth:
            print(f"min: returning heuristic {h(board, player)}, {None}")
            return h(board, player), None

        v, move = math.inf, None
        for a in board.get_actions(1 - player):
            transition = board.clone().play_action(a, 1 - player)
            v2, _ = max_value(transition, alpha, beta, depth+1)
            print(f"min: max_value returned {v2}, {None}")
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                print(f"min: pruning and returning {v}, {move}")
                return v, move
        
        print(f"min: returning end of min loop {v}, {move}")
        return v, move

    # print(max_depth)
    return max_value(board, -math.inf, math.inf, 0 )

def cutoff_depth(d):
    """A cutoff function that searches to depth d."""
    return lambda board, depth: depth > d

def heuristic(board : Board, player):
    score = board.get_score(player)
    return score



def mcts(current_state, player, max_sim):
    t = initTree(current_state, player)
    for _ in range(max_sim):
        n_leaf = select(t)
        n_child = expend(n_leaf, t, player)
        v = simulate(n_child, player)
        backpropagate(v, n_child)
    
    return bestAction(t)

class Node():
    def __init__(self, state, sims_count, sims_score, action_made, parent):
        self.state = state
        self.sims_count = sims_count
        self.sims_score = sims_score
        self.action_made = action_made
        self.parent = parent


def initTree(current_state, player):
    sims_count = 0
    sims_score = 0
    root = Node(current_state, sims_count, sims_score, None, None)
    tree = []
    for a in current_state.get_actions(player):
        transition = current_state.clone().play_action(a, player)
        child = Node(transition, sims_count, sims_score, a, root)
        tree.append(child)

    selection = random.choice(tree)
    v = simulate(selection, player)
    backpropagate(v, selection)

    return tree


def select(t):
    from numpy import log as ln
    max_ucb_node = None
    max_ucb = -math.inf
    for node in t:
        if node.sims_count == 0 or node.parent.sims_count == 0:
            ucb = 0 
        else:
            ucb = (node.sims_score / node.sims_count) + (math.sqrt(2) * math.sqrt(ln(node.parent.sims_count) / node.sims_count))
        
        if ucb > max_ucb:
            max_ucb_node = node
            max_ucb = ucb

    return max_ucb_node


def expend(n_leaf, tree, player):
    if n_leaf.sims_count > 0:
        for a in n_leaf.get_actions(player):
            transition = n_leaf.clone().play_action(a, player)
            child = Node(transition, 0, 0, a, n_leaf)
            tree.append(child)


def simulate(n_child, player):
    state = n_child.state.clone()
    playing = player

    while not state.is_finished:
        playing = 1 - playing
        rnd_action = random.choice(state.get_actions(playing)) #heurisitc instead ?
        state = state.play_action(rnd_action)
    
    return state.get_score(player)

def backpropagate(v, n_child):
    child = n_child

    while child.parent is not None:
        child.sims_count += 1
        child.sims_score += v
        child = child.parent


def bestAction(tree):
    max_sims_count = 0
    best_action = None
    for node in tree:
        if node.sims_count > max_sims_count:
            best_action = node.action_made
            max_sims_count = node.sims_count
    
    return best_action


if __name__ == "__main__":
    agent_main(MyAgent())

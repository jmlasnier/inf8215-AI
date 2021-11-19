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
        # _, move = h_alphabeta_search(board, player, 1, heuristic)
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



def mcts(board, player, max_sim):
    rootNode = initTree(board, player)
    for i in range(max_sim):
        print("select")
        promisingNode = select(rootNode)
        print("expend")
        nodeToExplore = expend(promisingNode)
        print("simulate")
        score = simulate(nodeToExplore)
        print("backpropagate")
        backpropagate(score, nodeToExplore)
        print(f"end of iteration {i}")
    
    return bestAction(rootNode)


class State():
    def __init__(self, board : Board, player, action_played_to_get_here = None, sims_count = 0, sims_score = 0):
        self.board = board
        self.sims_count = sims_count
        self.sims_score = sims_score
        self.player = player
        self.action_played_to_get_here = action_played_to_get_here


class Node():
    def __init__(self, state : State, parent = None, children = []):
        self.state = state
        self.parent = parent
        self.children = children


def initTree(board : Board, player):
    rootState = State(board, player)
    root = Node(rootState)
    # for a in board.get_actions(player):
    #     transition = board.clone().play_action(a, player)
    #     child = Node(transition, sims_count, sims_score, a, root)
    #     tree.append(child)

    # selection = random.choice(tree)
    # v = simulate(selection, player)
    # backpropagate(v, selection)

    return root


def select(rootNode : Node):
    from numpy import log as ln
    node : Node = rootNode
    while(len(node.children) != 0):
        max_ucb_node = None
        max_ucb = -math.inf
        for child in node.children:
            # if node.sims_count == 0 or node.parent.sims_count == 0:
            ucb = math.inf
            if child.state.sims_count != 0:
                ucb = (child.state.sims_score / child.state.sims_count) + (math.sqrt(2) * math.sqrt(ln(child.parent.state.sims_count) / child.state.sims_count))
            
            if ucb > max_ucb:
                max_ucb_node = child
                max_ucb = ucb

        node = max_ucb_node

    return node


def expend(n_leaf: Node):
    player = n_leaf.state.player
    for a in n_leaf.state.board.get_actions(player):
        transition = n_leaf.state.board.clone().play_action(a, player)
        newState = State(transition, 1 - player, a)
        newNode = Node(newState, n_leaf, [])
        n_leaf.children.append(newNode)

    n_toExplore = n_leaf
    if len(n_leaf.children) > 0:
        n_toExplore = random.choice(n_leaf.children)
    
    return n_toExplore


def simulate(n_explore : Node):
    board = n_explore.state.board.clone()
    player = n_explore.state.player
    while not board.is_finished:
        rnd_action = random.choice(board.get_actions(player)) #heurisitc instead ?
        board = board.play_action(rnd_action)
        player = 1 - player
    
    return board.get_score(player)

def backpropagate(v, n_child : Node):
    child = n_child

    while child is not None:
        child.state.sims_count += 1
        child.state.sims_score += v
        child = child.parent


def bestAction(rootNode : Node):
    print(rootNode.state.board)
    max_sims_count = -math.inf
    best_action = rootNode.children[0].state.action_played_to_get_here
    for child in rootNode.children:
        if child.state.sims_count > max_sims_count:
            best_action = child.state.action_played_to_get_here
            max_sims_count = child.state.sims_count
    
    return best_action


if __name__ == "__main__":
    agent_main(MyAgent())

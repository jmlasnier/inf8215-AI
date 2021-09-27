# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 1 ICI
    '''
    from util import Stack
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))


    #Get initial state
    state = problem.getStartState()
    #Initialize stack
    stack = Stack()
    #Push initial state to stack
    stack.push({'state':state, 'parentState':''})
    solution = []
    visited = []
    #While stack is not empty
    while not (stack.isEmpty()):
        #pop state off stack
        state = stack.pop()

        #if state is the goal state
        if problem.isGoalState(state['state']):

            while state['parentState'] != '':
                solution.append(state['moveTo'])
                state = state['parentState']
            solution.reverse()
            print('gg')
            return solution

        elif state['state'] not in visited:
            C = problem.getSuccessors(state['state'])
            # print(C)
            # C.reverse()
            for s in C:
                stack.push({'state':s[0], 'moveTo':s[1], 'parentState':state})
        
        visited.append(state['state'])

    return []



def breadthFirstSearch(problem):
    from util import Queue
    """Search the shallowest nodes in the search tree first."""


    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 2 ICI
    '''
        #Get initial state
    state = problem.getStartState()
    queue = Queue()
    #Push initial state to stack
    queue.push({'state':state, 'parentState':''})
    # queue.push({'state':(5,2), 'parentState':''})

    solution = []
    visited = []
    #While stack is not empty
    while not (queue.isEmpty()):
        #pop state off stack
        state = queue.pop()
        #if state is the goal state
        if problem.isGoalState(state['state']):

            while state['parentState'] != '':
                solution.append(state['moveTo'])
                state = state['parentState']
            solution.reverse()
            print('gg')
            print(solution)
            return solution

        elif state['state'] not in visited:
            C = problem.getSuccessors(state['state'])
            for s in C:
                queue.push({'state':s[0], 'moveTo':s[1], 'parentState':state})

        visited.append(state['state'])
    return []

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 3 ICI
    '''
    from util import PriorityQueue
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))



    #Get initial state
    state = problem.getStartState()
    
    #Initialize stack
    pQueue = PriorityQueue()

    #Push initial state to stack
    pQueue.push({'state':state, 'parentState':'', 'priority': 0}, 0)

    solution = []
    visited = []
    #While stack is not empty
    while not (pQueue.isEmpty()):
        #pop state off stack
        state = pQueue.pop()

        #if state is the goal state
        if problem.isGoalState(state['state']):

            while state['parentState'] != '':
                solution.append(state['moveTo'])
                state = state['parentState']
            solution.reverse()
            print('gg')
            return solution

        elif state['state'] not in visited:
            C = problem.getSuccessors(state['state'])
            for s in C:
                cost = state['priority'] + s[2]
                pQueue.push({'state':s[0], 'moveTo':s[1], 'priority':cost,'parentState':state}, cost)
        
        visited.append(state['state'])

    return []

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 4 ICI
    '''
    from util import PriorityQueue
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))



    #Get initial state
    state = problem.getStartState()
    
    #Initialize stack
    pQueue = PriorityQueue()

    #Push initial state to stack
    # gs = 0
    # hs = heuristic(state, problem)
    # cost = gs + hs
    # print('S cost: ',cost)
    pQueue.push({'state':state, 'parentState':'', 'priority': 0}, 0)

    solution = []
    visited = []
    #While stack is not empty
    while not (pQueue.isEmpty()):
        #pop state off stack
        state = pQueue.pop()

        #if state is the goal state
        if problem.isGoalState(state['state']):

            while state['parentState'] != '':
                solution.append(state['moveTo'])
                state = state['parentState']
            solution.reverse()
            print('gg')
            return solution

        elif state['state'] not in visited:
            C = problem.getSuccessors(state['state'])
            for s in C:

                hs = heuristic(s[0], problem)
                moveCost = state['priority'] + s[2]
                priority = hs + moveCost

                pQueue.push({'state':s[0], 'moveTo':s[1], 'priority':moveCost,'parentState':state}, priority)
        
        visited.append(state['state'])

    return []

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

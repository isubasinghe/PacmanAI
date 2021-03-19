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

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
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
    """
    "*** YOUR CODE HERE ***"
    mystack = util.Stack()
    startNode = (problem.getStartState(), '', 0, [])
    mystack.push(startNode)
    visited = set()
    while mystack :
        node = mystack.pop()
        state, action, cost, path = node
        if state not in visited :
            visited.add(state)
            if problem.isGoalState(state) :
                path = path + [(state, action)]
                break;
            succNodes = problem.expand(state)
            for succNode in succNodes :
                succState, succAction, succCost = succNode
                newNode = (succState, succAction, cost + succCost, path + [(state, action)])
                mystack.push(newNode)
    actions = [action[1] for action in path]
    del actions[0]
    return actions

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    #COMP90054 Task 1, Implement your A Star search algorithm here
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    current = problem.getStartState()
    pq = util.PriorityQueue()
    pq.push((current, '', 0, []), 0)

    # we will reuse bestG as the closed set as well to save on memory
    bestG = dict()

    while not pq.isEmpty():
        state, action, cost, path = pq.pop()
        
        skip = state in bestG
        if skip:
            skip = cost >= bestG[state]
        
        if skip:
            continue
        
        bestG[state] = cost

        if problem.isGoalState(state):
            path = path + [(state, action)]
            break
        
        for succNode in problem.expand(state):
            succState, succAction, succCost = succNode
            newNode = (succState, succAction, cost + succCost, path + [(state, action)])
            h = heuristic(succState, problem)
            if h < float('inf'):
                pq.push(newNode, cost + succCost + h)
    
    actions = [action[1] for action in path]
    del actions[0]
    return actions


def rbfs(problem, node, fLimit, h):
    state, action, cost, path = node
    if problem.isGoalState(state):
        pass

    successors = []
    
    bestSuccs = util.PriorityQueue()


    for succNode in problem.expand(state):
        succState, succAction, succCost = succNode
        f = max(cost + succCost, fLimit)
        node = (succState, succAction, cost + succCost, path + [(state, action)], f)
        successors.append(node)
        if len(bestSuccs.heap) < 2:
            bestSuccs.push(node, 1/f)
        else:
            item, score = bestSuccs.pop()
            istate, iaction, icost, ipath, iscore = item
            if iscore > f:
                bestSuccs.push(node, 1/f)
            else:
                bestSuccs.push(item, 1/iscore)
    
    if len(successors) == 0:
        return None
    
    alt, _ = bestSuccs.pop()
    best, _ = bestSuccs.pop()

    astate, aaction, acost, apath, af = alt
    bstate, baction, bcost, bpath, bf = best
    while True:
        if bf > fLimit:
            return None
        
        

    return []

        
def recursivebfs(problem, heuristic=nullHeuristic) :
    node = (problem.getStartState(), '', 0, [])
    return rbfs(problem, node, float('inf'), heuristic)
    

    
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
rebfs = recursivebfs

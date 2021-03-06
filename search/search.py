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

import typing
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
    return [s, s, w, s, w, w, s, w]


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
    while mystack:
        node = mystack.pop()
        state, action, cost, path = node
        if state not in visited:
            visited.add(state)
            if problem.isGoalState(state):
                path = path + [(state, action)]
                break
            succNodes = problem.expand(state)
            for succNode in succNodes:
                succState, succAction, succCost = succNode
                newNode = (succState, succAction, cost +
                           succCost, path + [(state, action)])
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
    # COMP90054 Task 1, Implement your A Star search algorithm here
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
            newNode = (succState, succAction, cost +
                       succCost, path + [(state, action)])
            h = heuristic(succState, problem)
            if h < float('inf'):
                pq.push(newNode, cost + succCost + h)

    actions = [action[1] for action in path]
    del actions[0]
    return actions


Path = typing.List[typing.Tuple[typing.Any, str]]


class RBFSNode:
    def __init__(self, state: typing.Any, action: str, cost: float, path: Path,  f: float):
        self.state = state
        self.action = action
        self.cost = cost
        self.path = path
        self.f = f

    def getState(self) -> typing.Any:
        return self.state

    def solution(self):
        self.path = self.path + [(self.state, self.action)]
        actions = [action[1] for action in self.path]
        del actions[0]
        return actions, self.f

    def __str__(self):
        return f"state={self.state}, action={self.action}, cost={self.cost}, path=${self.path}, f={self.f}"


def rbfs(problem, node, fLimit, h) -> typing.Tuple[typing.Any, float]:
    if problem.isGoalState(node.getState()):
        return node.solution()

    succ: typing.List[RBFSNode] = []

    for child in problem.expand(node.getState()):
        succState, succAction, succCost = child
        totCosts: float = node.cost + succCost
        f: float = max(totCosts + h(succState, problem), node.f)
        path: Path = node.path + [(node.state, node.action)]
        childNode = RBFSNode(succState, succAction, totCosts, path, f)
        succ.append(childNode)

    if len(succ) == 0:
        return None, float('inf')

    while True:
        succ.sort(key=lambda x: x.f)
        best = succ[0]
        if best.f > fLimit:
            return None, best.f
        alt: float = float('inf')

        if len(succ) > 1:
            alt = succ[1].f

        result, best.f = rbfs(problem, best, min(fLimit, alt), h)
        if result != None:
            return result, best.f


def recursivebfs(problem, heuristic=nullHeuristic):
    start = problem.getStartState()
    node = RBFSNode(start, '', 0, [], heuristic(start, problem))
    actions, f = rbfs(problem, node, float('inf'), heuristic)
    return actions


def capsuleAwareAStar(problem, capsules, heuristic=nullHeuristic):
    # COMP90054 Task 1, Implement your A Star search algorithm here
    current = problem.getStartState()
    pq = util.PriorityQueue()
    pq.push((current, '', 0, [], capsules), 0)

    # we will reuse bestG as the closed set as well to save on memory
    bestG = dict()

    while not pq.isEmpty():
        state, action, cost, path, caps = pq.pop()

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

            newCaps = capsules.copy()

            if succState in caps:
                newCaps.remove(succState)
                succCost = 0

            newNode = (succState, succAction, cost +
                       succCost, path + [(state, action)], newCaps)
            h = heuristic(succState, problem)
            if h < float('inf'):
                pq.push(newNode, cost + succCost + h)
    return cost

    # Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
rebfs = recursivebfs

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
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # depth1 = problem.getSuccessors(problem.getStartState())
    # print("Start's successors:", depth1)
    # print("1's successors:", problem.getSuccessors(depth1[0][0]))

    # Start: (5, 5)
    # Is the start a goal? False
    # Start's successors: [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
    # 1's successors: [((5, 5), 'North', 1), ((5, 3), 'South', 1)]

    # print('problem help:', help(problem))

    start_state = problem.getSuccessors(problem.getStartState())
    fringe = [list(pos) + [[]] for pos in start_state]
    visited_leafs = [problem.getStartState()[0]]
    counter = 0
    while(len(fringe) > 0):
        leaf = fringe.pop()
        visited_leafs.append(leaf[0])
        
        if isinstance(leaf, tuple):
            leaf = list(leaf)
            leaf.append([])
        #print(leaf)
        if problem.isGoalState(leaf[0]):
            soln = leaf[-1]
            soln.append(leaf[1])
            return soln#[1:]
        children = problem.getSuccessors(leaf[0])
        for c in children:
            if c[0] in visited_leafs:
                continue
            c = list(c)
            c.append(leaf[-1]+[leaf[1]])
            fringe.append(c)

        counter += 1
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    start_state = problem.getSuccessors(problem.getStartState())
    fringe = [list(pos) + [[]] for pos in start_state][::-1]
    visited_leafs = [problem.getStartState()[0]]
    counter = 0
    while(len(fringe) > 0):
        leaf = fringe.pop()
        if leaf[0] not in visited_leafs:
            
            visited_leafs.append(leaf[0])
            
            if isinstance(leaf, tuple):
                leaf = list(leaf)
                leaf.append([])
            #print(leaf)
            if problem.isGoalState(leaf[0]):
                soln = leaf[-1]
                soln.append(leaf[1])
                return soln#[1:]
            children = problem.getSuccessors(leaf[0])
            for c in children:
                if c[0] in visited_leafs:
                    continue
                c = list(c)
                c.append(leaf[-1]+[leaf[1]])
                fringe.insert(0,c)
            
        counter += 1
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    start_state = problem.getSuccessors(problem.getStartState())
    fringe = [list(pos) + [[[], pos[2]]] for pos in start_state]
    visited_leafs = [problem.getStartState()[0]]
    counter = 0
    while(len(fringe) > 0):
        fringe.sort(key= lambda x : x[-1][-1], reverse=True)
        leaf = fringe.pop()
        if leaf[0] not in visited_leafs:
            
            visited_leafs.append(leaf[0])
            
            if isinstance(leaf, tuple):
                leaf = list(leaf)
                leaf.append([[], leaf[2]])
            #print(leaf)
            if problem.isGoalState(leaf[0]):
                soln = leaf[-1][0]
                soln.append(leaf[1])
                return soln
            children = problem.getSuccessors(leaf[0])
            for c in children:
                if c[0] in visited_leafs:
                    continue
                c = list(c)
                c.append([leaf[-1][0]+[leaf[1]], leaf[-1][-1]+c[2]])
                fringe.append(c)
        # if counter > 3:
        #     break
        counter += 1
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    start_state = problem.getSuccessors(problem.getStartState())
    fringe = [list(pos) + [[[], pos[2], heuristic(pos[0], problem=problem)]] for pos in start_state]
    visited_leafs = [problem.getStartState()[0]]
    counter = 0
    while(len(fringe) > 0):
        fringe.sort(key= lambda x : x[-1][-2] + x[-1][-1], reverse=True)
        #print(fringe)
        leaf = fringe.pop()
        if leaf[0] not in visited_leafs:
            
            visited_leafs.append(leaf[0])
            
            if isinstance(leaf, tuple):
                leaf = list(leaf)
                leaf.append([[], leaf[2], heuristic(leaf[0], problem=problem)])
            #print(leaf)
            if problem.isGoalState(leaf[0]):
                soln = leaf[-1][0]
                soln.append(leaf[1])
                return soln
            children = problem.getSuccessors(leaf[0])
            for c in children:
                if c[0] in visited_leafs:
                    continue
                c = list(c)
                c.append([leaf[-1][0]+[leaf[1]], leaf[-1][1]+c[2], heuristic(c[0], problem=problem)])
                fringe.append(c)
        # if counter > 3:
        #     break
        counter += 1
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

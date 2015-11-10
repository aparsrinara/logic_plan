# logicPlan.py
# ------------
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
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    a_or_b = A | B
    notA, notB = ~A, ~B
    notB_or_C = notB | C
    notA_iff = notA % notB_or_C
    notA_or_else = logic.disjoin([notA,notB,C])

    return logic.conjoin([(a_or_b),(notA_iff),(notA_or_else)])

    util.raiseNotDefined()

def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    A, B, C, D = logic.Expr('A'), logic.Expr('B'), logic.Expr('C'), logic.Expr('D')
    C_iff = C % logic.disjoin([B,D])
    A_imp = A >> logic.conjoin([~B, ~D])
    nots = ~(logic.conjoin([B, ~C])) >> A
    notD = ~D >> C

    return logic.conjoin([C_iff, A_imp, nots, notD])
    util.raiseNotDefined()

def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    time_1_alive = logic.PropSymbolExpr('WumpusAlive', 1)
    time_0_alive = logic.PropSymbolExpr("WumpusAlive", 0)
    time_0_born = logic.PropSymbolExpr("WumpusBorn", 0)
    time_0_killed = logic.PropSymbolExpr("WumpusKilled", 0)
    alive_and_notkilled = time_0_alive & ~time_0_killed
    notalive_and_born = ~time_0_alive & time_0_born
    first_exp = time_1_alive % (alive_and_notkilled | notalive_and_born)
    second_exp = ~(time_0_alive & time_0_born)
    return logic.conjoin([first_exp, second_exp, time_0_born])
    util.raiseNotDefined()

def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    cnf = logic.to_cnf(sentence)
    return logic.pycoSAT(cnf)

    util.raiseNotDefined()

def atLeastOne(literals) :
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single 
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"

    return logic.disjoin(literals)

    util.raiseNotDefined()


def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"

    allComp = []
    for l in literals:
        for i in literals[literals.index(l)+1:]:
            allComp.append(~l | ~i)
    return logic.conjoin(allComp)


    util.raiseNotDefined()


def exactlyOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    return atLeastOne(literals) & atMostOne(literals)



def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    l_action = []
    psb = []
    maxI = 0
    for key in model:
        if model[key]:
            action = logic.PropSymbolExpr.parseExpr(key)
            if action[0] in actions:
                l_action.append(action)
                for i in range(len(action)):
                    if i > 0:
                        if int(action[i]) > maxI:
                            maxI = int(action[i])
    plan = []
    for i in range(maxI+1):
        for action in l_action:
            for j in range(len(action)):
                if j > 0:
                    if int(action[j]) == i:
                        plan.append(action[0])

    return plan

    util.raiseNotDefined()


def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"
    pos = logic.PropSymbolExpr(pacman_str, x, y, t)
    listAdj = [(x, y+1), (x-1, y), (x+1, y), (x, y-1)]
    lst = []
    i = 0
    for l in listAdj:
        if not walls_grid[l[0]][l[1]]:
            if l == (x, y+1):
                e = logic.PropSymbolExpr(pacman_str, x, y+1, t-1) & logic.PropSymbolExpr("South", t-1)
            elif l == (x-1, y):
                e = logic.PropSymbolExpr(pacman_str, x-1, y, t-1) & logic.PropSymbolExpr("East", t-1)
            elif l == (x+1, y):
                e = logic.PropSymbolExpr(pacman_str, x+1, y, t-1) & logic.PropSymbolExpr("West", t-1)
            else:
                e = logic.PropSymbolExpr(pacman_str, x, y-1, t-1) & logic.PropSymbolExpr("North", t-1)
            if i == 0:
                r = e
            else:
                r = r | e
            i = i + 1
    return pos % r
   

def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    
    "*** YOUR CODE HERE ***"
    (x, y) = problem.getStartState();
    (v, w) = problem.getGoalState();
    initial = []
    initial.append(logic.PropSymbolExpr(pacman_str, x, y, 0))
    for r in xrange(1,width+1):
        for c in xrange(1, height+1):
            if not walls[r][c] and ((r,c) != (x,y)):
                initial.append(~(logic.PropSymbolExpr(pacman_str, r,c,0)))

    init = logic.conjoin(initial)

    lst = []
    for t in range(1,51):
        for r in xrange(1,width+1):
            for c in xrange(1, height+1):
                if not walls[r][c]:
                    lst.append(pacmanSuccessorStateAxioms(r, c, t, walls))

        d = []
        d.append(logic.PropSymbolExpr(game.Directions.NORTH,t-1))
        d.append(logic.PropSymbolExpr(game.Directions.SOUTH,t-1))
        d.append(logic.PropSymbolExpr(game.Directions.EAST,t-1))
        d.append(logic.PropSymbolExpr(game.Directions.WEST,t-1))
        lst.append(exactlyOne(d))
        lisst = logic.conjoin(lst)
        result = lisst & logic.PropSymbolExpr(pacman_str, v, w, t) & init
        model = findModel(result)
        if model != False: 
            seq = extractActionSequence(model, [game.Directions.NORTH, game.Directions.SOUTH,game.Directions.EAST, game.Directions.WEST])
            return seq

def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    "*** YOUR CODE HERE ***"
    initialState = problem.getStartState()

    foodGrid = initialState[1]

    
    (x, y) = initialState[0]
    initial = []
    initial.append(logic.PropSymbolExpr(pacman_str, x, y, 0))
    foodLoc = []
    foodLoac = []
    for r in xrange(1,width+1):
        for c in xrange(1, height+1):
            if not walls[r][c] and ((r,c) != (x,y)):
                initial.append(~(logic.PropSymbolExpr(pacman_str, r,c,0)))
                if foodGrid[r][c]:
                    foodLoc.append(logic.PropSymbolExpr(pacman_str,r,c,0))
                    foodLoac.append((r,c))
    init = logic.conjoin(initial)

    lst = []
    for t in range(1,51):
        for r in xrange(1,width+1):
            for c in xrange(1, height+1):
                if not walls[r][c]:
                    lst.append(pacmanSuccessorStateAxioms(r, c, t, walls))

        d = []
        d.append(logic.PropSymbolExpr(game.Directions.NORTH,t-1))
        d.append(logic.PropSymbolExpr(game.Directions.SOUTH,t-1))
        d.append(logic.PropSymbolExpr(game.Directions.EAST,t-1))
        d.append(logic.PropSymbolExpr(game.Directions.WEST,t-1))
        for food in foodLoac:
            foodLoc[foodLoac.index(food)] = foodLoc[foodLoac.index(food)] | logic.PropSymbolExpr(pacman_str,food[0],food[1],t)
        goalState = logic.conjoin(foodLoc)
        lst.append(exactlyOne(d))
        lisst = logic.conjoin(lst)
        result = lisst & init & goalState
        model = findModel(result)
        if model != False: 
            seq = extractActionSequence(model, [game.Directions.NORTH, game.Directions.SOUTH,game.Directions.EAST, game.Directions.WEST])
            return seq
   
               
    util.raiseNotDefined()

def ghostPositionSuccessorStateAxioms(x, y, t, ghost_num, walls_grid):
    """
    Successor state axiom for patrolling ghost state (x,y,t) (from t-1).
    Current <==> (causes to stay) | (causes of current)
    GE is going east, ~GE is going west 
    """
    pos_str = ghost_pos_str+str(ghost_num)
    east_str = ghost_east_str+str(ghost_num)

    pos = logic.PropSymbolExpr(pos_str, x, y, t)
    listAdj = [(x-1, y), (x+1, y)]
    lst = []
    for l in listAdj:
        if not walls_grid[l[0]][l[1]]:
            if l == (x-1, y):
                e = logic.conjoin([logic.PropSymbolExpr(pacman_str, x-1, y, t-1), logic.PropSymbolExpr(east_str, t-1)])
            else:
                e = logic.conjoin([logic.PropSymbolExpr(pacman_str, x+1, y, t-1), ~(logic.PropSymbolExpr(east_str, t-1))])
            lst.append(e)
    if (len(lst) == 0):
        return pos % pos
    r = logic.disjoin(lst)
    return pos % r
    "*** YOUR CODE HERE ***"
    return logic.Expr('A') # Replace this with your expression

def ghostPositionSuccessorStateAxioms(x, y, t, ghost_num, walls_grid):
    """
    Successor state axiom for patrolling ghost state (x,y,t) (from t-1).
    Current <==> (causes to stay) | (causes of current)
    GE is going east, ~GE is going west 
    """
    pos_str = ghost_pos_str+str(ghost_num)
    east_str = ghost_east_str+str(ghost_num)

    pos = logic.PropSymbolExpr(pos_str, x, y, t)
    listAdj = [(x-1, y), (x+1, y)]
    lst = []
    for l in listAdj:
        if not walls_grid[l[0]][l[1]]:
            if l == (x-1, y):
                e = logic.conjoin([logic.PropSymbolExpr(pos_str, x-1, y, t-1), logic.PropSymbolExpr(east_str, t-1)]) 
            else:
                e = logic.conjoin([logic.PropSymbolExpr(pos_str, x+1, y, t-1), ~(logic.PropSymbolExpr(east_str, t-1))])
            lst.append(e)
    if walls_grid[x-1][y] & walls_grid[x+1][y]: #if there are walls on both sides and ghost cannot move
       lst.append(logic.PropSymbolExpr(pos_str, x, y, t-1))
    if (len(lst) == 0):
        return pos % pos
    r = logic.disjoin(lst)
    return pos % r


def ghostDirectionSuccessorStateAxioms(t, ghost_num, blocked_west_positions, blocked_east_positions):
    """
    Successor state axiom for patrolling ghost direction state (t) (from t-1).
    west or east walls.
    Current <==> (causes to stay) | (causes of current)
    """
    # iterate over 
    # blocked east and blocked west disjoin 
    pos_str = ghost_pos_str+str(ghost_num)
    east_str = ghost_east_str+str(ghost_num)
    lst = []
    lst3 = []
    for (x, y) in blocked_east_positions:
        lst.append(logic.PropSymbolExpr(pos_str, x, y, t))
    east = ~(logic.disjoin(lst))
    east = logic.PropSymbolExpr(east_str, t-1) & east
    lst2 = []
    for (x, y) in blocked_west_positions:
        lst2.append(logic.PropSymbolExpr(pos_str, x, y, t))   
    west = logic.disjoin(lst2)
    west = ~(logic.PropSymbolExpr(east_str, t-1)) & west
    return logic.PropSymbolExpr(east_str, t) % (east | west)
   
   


def pacmanAliveSuccessorStateAxioms(x, y, t, num_ghosts):
    """
    Successor state axiom for patrolling ghost state (x,y,t) (from t-1).
    Current <==> (causes to stay) | (causes of current)
    """
    ghost_strs = [ghost_pos_str+str(ghost_num) for ghost_num in xrange(num_ghosts)]

    alive = logic.PropSymbolExpr(pacman_alive_str, t)
    lst = []
    e = []
    for g in ghost_strs:
        e.append(~logic.PropSymbolExpr(g, x, y, t-1))
        e.append(~logic.PropSymbolExpr(g, x, y, t))
    q = logic.conjoin(e)
    lst.append(q)
    lst.append(~logic.PropSymbolExpr(pacman_str, x, y, t))
    res = logic.disjoin(lst)
    if len(lst) == 0:
        return alive % alive 
    return alive % (logic.conjoin([logic.PropSymbolExpr(pacman_alive_str, t-1), res]))


def foodGhostLogicPlan(problem):
    """
    Given an instance of a FoodGhostPlanningProblem, return a list of actions that help Pacman
    eat all of the food and avoid patrolling ghosts.
    Ghosts only move east and west. They always start by moving East, unless they start next to
    and eastern wall. 
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    "*** YOUR CODE HERE ***"
    initialState = problem.getStartState();
    (x, y) = initialState[0]
    foodGrid = initialState[1]
    initial = []
    num_ghosts = len(problem.getGhostStartStates())
    initial.append(logic.PropSymbolExpr(pacman_str, x, y, 0) & logic.PropSymbolExpr(pacman_alive_str, 0))
    gStart = []
    for ghost_num in range(0, num_ghosts):
        gStart.append(logic.PropSymbolExpr(ghost_pos_str+str(ghost_num), problem.getGhostStartStates()[ghost_num].getPosition()[0], problem.getGhostStartStates()[ghost_num].getPosition()[1], 0))
    foodLoc = []
    foodLoac = []
    blockedWest = []
    blockedEast = []
    for r in xrange(1, width+1):
        for c in xrange(1, height+1):
            if not walls[r][c]:
                if ((r,c) != (x,y)):
                    initial.append(~(logic.PropSymbolExpr(pacman_str, r, c, 0)))
                for ghost_num in range(0, num_ghosts):
                    if ((r, c) != (problem.getGhostStartStates()[ghost_num].getPosition()[0], problem.getGhostStartStates()[ghost_num].getPosition()[1])):
                        a = ~(logic.PropSymbolExpr(ghost_pos_str+str(ghost_num), r, c, 0))
                        gStart.append(a)
                if not walls[r][c] and walls[r+1][c]:
                    blockedEast.append((r, c))
                if not walls[r][c] and walls[r-1][c]:
                    blockedWest.append((r, c))
                if foodGrid[r][c]:
                    foodLoc.append(logic.PropSymbolExpr(pacman_str,r,c,0))
                    foodLoac.append((r,c))
    for ghost_num in range(0, num_ghosts):
        startPos = (problem.getGhostStartStates()[ghost_num].getPosition()[0], problem.getGhostStartStates()[ghost_num].getPosition()[1])
        if startPos in blockedEast:
            gStart.append(~logic.PropSymbolExpr(ghost_east_str+str(ghost_num), 0))
        else:
            gStart.append(logic.PropSymbolExpr(ghost_east_str+str(ghost_num), 0))

    init = logic.to_cnf(logic.conjoin(initial + gStart))
    

    pacmanAliveList = []
    ghostDirList = []
    pacmanPositionList = []
    ghostPositionList = []
    lst = []
    for t in range(1, 51):
        for ghost_num in range(0, num_ghosts):
            ghostDirList.append(ghostDirectionSuccessorStateAxioms(t, ghost_num, blockedWest, blockedEast))
        for r in xrange(1, width+1):
            for c in xrange(1, height+1):
                if not walls[r][c]:
                    pacmanPositionList.append(pacmanSuccessorStateAxioms(r, c, t, walls))
                    pacmanAliveList.append(pacmanAliveSuccessorStateAxioms(r, c, t, num_ghosts))
                    for ghost_num in range(0, num_ghosts):
                        ghostPositionList.append(ghostPositionSuccessorStateAxioms(r, c, t, ghost_num, walls))            
        d = []
        d.append(logic.PropSymbolExpr(game.Directions.NORTH, t-1))
        d.append(logic.PropSymbolExpr(game.Directions.SOUTH, t-1))
        d.append(logic.PropSymbolExpr(game.Directions.EAST, t-1))
        d.append(logic.PropSymbolExpr(game.Directions.WEST, t-1))
        lst.append(exactlyOne(d))
        for food in foodLoac:
            foodLoc[foodLoac.index(food)] = foodLoc[foodLoac.index(food)] | logic.PropSymbolExpr(pacman_str,food[0],food[1],t)
        goalState = logic.to_cnf(logic.conjoin(foodLoc) & logic.PropSymbolExpr(pacman_alive_str, t))
        lisst = logic.to_cnf(logic.conjoin(list(set(pacmanPositionList)) + list(set(pacmanAliveList)) + list(set(ghostPositionList)) + list(set(ghostDirList)) + list(set(lst))))
        result = lisst & init & goalState
        model = logic.pycoSAT(result)
        if model != False:
            seq = extractActionSequence(model, [game.Directions.NORTH, game.Directions.SOUTH,game.Directions.EAST, game.Directions.WEST])
            return seq
    util.raiseNotDefined()
# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan
fglp = foodGhostLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
 

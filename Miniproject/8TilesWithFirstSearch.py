"""
Problem mapping
A list containing 9 ints represents the 3x3 gameboard: GB = [0,1,2,3,4,5,6,7,8]
numbers 1-8 will be the "actual" numbered tile,
number 0 will represent the "blank space"
for the sake of simplicity the goal state will be having the list ordered as shown in line 3
                                                      |_|1|2|
meaning the "real world" grid would look like this -> |3|4|5|
                                                      |6|7|8|
which looks kinda dumb, but it looks better as a list so I am using that as the goal
Valid actions on the game board is to switch 0's location with any non-diagonal neighbor tile
In order to translate the "movement" of the tiles to code there is some things to keep in mind
moving 0 up is not valid if it is in places    GB[0],GB[1] or GB[2]
moving 0 down is not valid if it is in places  GB[6],GB[7] or GB[8]
moving 0 left is not valid if it is in places  GB[0],GB[3] or GB[6]
moving 0 right is not valid if it is in places GB[2],GB[5] or GB[8]

The possible Actions is to move the zero tile up, down, left or right and move the neighbor tile into zero's old space

to move up:     zeroTileIndex, aboveTileIndex = aboveTileIndex, zeroTileIndex
to move down:   zeroTileIndex, belowTileIndex = belowTileIndex, zeroTileIndex
to move left:   zeroTileIndex, leftTileIndex  = leftTileIndex,  zeroTileIndex
to move right:  zeroTileIndex, rigthTileIndex = rigthTileIndex, zeroTileIndex
"""

class Node:
    """A Node class with instance attributes suggested for use in search algorithms by Russell and Norvig (2010)."""
    # constructor for defining the instance attributes
    def __init__(self, state=None, parent=None, action=None, path_cost=0):
        self.state = state  # tuple
        self.parent = parent  # Node object
        self.action = action  # tuple; the action applied to the parent state that results in self.state
        self.path_cost = path_cost  # cost(p); equivalent to depth when each action has a cost of 1
        self.depth = 0  # level in search tree
        if parent:
            self.depth = parent.depth + 1

"""
First off I need a list to contain how the board looks when we start
and another for how the solution looks
"""

"And I need nodes for them both for testing"


"""
next I need a function which takes in a state and returns all the possible childstates the parent can produce
"""
def findPossibleStates(parent):
    parentState = parent.state
    zeroTile = parentState.index(0) #finds the element in the list which has the vale 0
    possibleMovements = [] #this list will be used to store possible states after a valid move,
                           # i also need to save these valid moves in a Node object

    if zeroTile >= 3: #checks if zero is in a place where moving up is valid i.e. not GB[0],GB[1] or GB[2]
        newMove = list(parentState) # creates a copy of the current state, which will be modified to make a child state
        newMove[zeroTile],  newMove[zeroTile - 3] = newMove[zeroTile - 3], newMove[zeroTile]
        #Switch the around the zero tile and one above it on the newMove list, remember the tile above is always
        #the element in the list that is 3 places back
        possibleMovements.append(Node(newMove,parent,"up",parent.depth + 1))#save this movement or child as a node in the possibleMovements list

    """
    Now we do the same thing for down
    """
    if zeroTile <= 5: #checks if zero is in a place where moving down is valid i.e. not GB[6],GB[7] or GB[8]
        newMove = list(parentState)
        newMove[zeroTile],  newMove[zeroTile + 3] = newMove[zeroTile + 3], newMove[zeroTile]
        possibleMovements.append(Node(newMove,parent,"down",parent.depth + 1))

    """
    Left and right are a bit more tricky, since I can't use ">=" or "<="
    instead I can use % to check if zeroTile's has a value that is divisible by 3
    If it is then zero has to be on GB[0],GB[3] or GB[6] where moving left is invalid
    """
    if zeroTile % 3 != 0: #if zeroTile is NOT on GB[0],GB[3] or GB[6]
        newMove = list(parentState)
        newMove[zeroTile],  newMove[zeroTile - 1] = newMove[zeroTile - 1], newMove[zeroTile]
        possibleMovements.append(Node(newMove,parent,"left",parent.depth + 1))

    """
    with a little modification I can use the same trick for checking if moving right is valid
    moving right is invalid if zero is on GB[2],GB[5] or GB[8]
    what these three have in common is that if I add 1 to them I get a number that is divisible by 3
    """
    if (zeroTile + 1) % 3 != 0: #if zeroTile is NOT on GB[2],GB[5] or GB[8]
        newMove = list(parentState)
        newMove[zeroTile], newMove[zeroTile + 1] = newMove[zeroTile + 1], newMove[zeroTile]
        possibleMovements.append(Node(newMove,parent,"right",parent.depth + 1))

    return possibleMovements

"""
Next, a functions for comparing the states and their children to the goal state until a match is reached
"""


def breadthFirst(startState, goalState):
    if startState == goalState:
        print("solution found", startState)
        print(startState)
        #return construct_path(Node(startState, None, None), startState)
    frontier = [Node(startState, None, None)]
    visited = []
    actionCost = 0
    while frontier:
        parent = frontier.pop(0)
        for child in findPossibleStates(parent):
            if child.state == goalState:
                return print(child.state, "Solution Found, Path cost ",actionCost),
            if child.state not in visited:
                visited.append(child.state)
                frontier.append(child)
                print(child.state)
                actionCost += 1

def depthFirst(startState, goalState):
    if startState == goalState:
        print("solution found", startState)
        print(startState)
        #return construct_path(Node(startState, None, None), startState)
    frontier = [Node(startState, None, None)]
    visited = []
    actionCost = 0
    while frontier:
        parent = frontier.pop()
        for child in findPossibleStates(parent):
            if child.state == goalState:
                return print(child.state, "Solution Found, Path cost ",actionCost),
            if child.state not in visited:
                visited.append(child.state)
                frontier.append(child)
                print(child.state)
                actionCost += 1


def construct_path(final_node, startState):
    """Constructs the path from the initial state to the goal state by working backwards through parents starting from
    the goal node.
    """
    state_path = []  # initialize a path to hold states which comprise a solution
    action_path = []  # initialize a path to hold actions which comprise a solution
    while final_node.state != startState:
        state_path.append(final_node.state)
        action_path.append(final_node.action)
        final_node = final_node.parent
    state_path.append(final_node.state)
    action_path.append(final_node.action)
    return state_path[::-1], action_path[::-1]  # return path from initial state to goal state

def breadth_first_search(initial_state, goal_state):
    """Breadth-first search algorithm expands all child nodes of a parent node at each level in search for a state which
  matches the specified goal state. In this implementation, a list is treated as a queue by always removing elements
  from the front and appending elements to the back.
  """
    if initial_state == goal_state:
        return construct_path(Node(initial_state, None, None), initial_state)
    # QUEUE: initialize a list to hold nodes to be expanded with the root node of the initial state as the only element
    frontier = [Node(initial_state, None, None)]
    reached = set()  # initialize an empty set to hold visited node states
    while frontier:
        parent = frontier.pop(0)  # remove the first node added (i.e., shallowest)
        # check whether or not a solution has been found
        for child in findPossibleStates(parent):
            if child.state == goal_state:
                return construct_path(child, initial_state)
            if child.state not in reached:  # valid state that has not previously been explored
                reached.add(child.state)
                frontier.append(child)
    return [], []  # no solution found; return empty state and action paths

startState = [2, 8, 3, 1, 6, 4, 7, 0, 5]
goalState  = [1, 2, 3, 8, 0, 4, 7, 6, 5]
"""
                                                          |1|2|3|
meaning the "real world" Solution would look like this -> |8|_|4|
                                                          |7|6|5|
"""
breadthFirst(startState, goalState)
#depthFirst(startState, goalState)

"""
Problem mapping
A list containing 9 ints represents the 3x3 gameboard: GB = [0,1,2,3,4,5,6,7,8]
numbers 1-8 will be the "actual" numbered tile,
number 0 will represent the "blank space"
The initial state will be GB = [2, 8, 3, 1, 6, 4, 7, 0, 5]
                                                      |2|8|3|
meaning the "real world" grid would look like this -> |1|6|4|
                                                      |7|_|5|
and the goal state will be GB = [1, 2, 3, 8, 0, 4, 7, 6, 5]
                                                      |1|2|3|
meaning the "real world" grid would look like this -> |8|0|4|
                                                      |7|6|5|
I took these states from slide 25 from lecture 4

Valid actions on the game board is to switch 0's location with any non-diagonal neighbor tile
In order to translate the "movement" of the tiles to code there is some things to keep in mind
moving 0 up is not valid if it is in places    GB[0],GB[1] or GB[2]
moving 0 down is not valid if it is in places  GB[6],GB[7] or GB[8]
moving 0 left is not valid if it is in places  GB[0],GB[3] or GB[6]
moving 0 right is not valid if it is in places GB[2],GB[5] or GB[8]

"""
import random


class Node:
    """
    A Node class with instance attributes suggested for use in search algorithms by Russell and Norvig (2010).
    I got this from the cardinals and canibals exersice
    """
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
I need a function which takes in a parent Node and returns all the possible child Nodes the parent can produce
"""
def findPossibleStates(parent):
    parentState = parent.state #find the state contained in parent Node
    zeroTile = parentState.index(0) #finds the element in the list which has the value 0
    possibleMovements = [] #this list will be used to store possible states after a valid move,
                           # i also need to save these valid moves in a Node object

    if zeroTile >= 3: #checks if zero is in a place where moving up is valid i.e. not GB[0],GB[1] or GB[2]
        newMove = list(parentState) # creates a copy of the current state, which will be modified to make a child state
        newMove[zeroTile],  newMove[zeroTile - 3] = newMove[zeroTile - 3], newMove[zeroTile]
        #Switch the around the zero tile and one above it on the newMove list, remember the tile above is always
        #the element in the list that is 3 places back
        possibleMovements.append(Node(newMove,parent,"up",parent.depth + 1))#save this child as a node in the possibleMovements list

    """
    Now we do the same thing for down
    """
    if zeroTile <= 5: #checks if zero is in a place where moving down is valid i.e. not GB[6],GB[7] or GB[8]
        newMove = list(parentState)
        newMove[zeroTile],  newMove[zeroTile + 3] = newMove[zeroTile + 3], newMove[zeroTile]
        possibleMovements.append(Node(newMove,parent,"down",parent.depth + 1))

    """
    Left and right are a bit more tricky, since I can't use ">=" or "<="
    instead I can use % to check whether zeroTile's has a value that is divisible by 3
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
Now I have the code for generating child nodes, now I need to start searching
"""

def breadthFirst(startState, goalState):
    actionCost = 0 #an int for counting how many steps are taken to find solution
    if startState == goalState: #Check if we already have a solution, unlikely but good to have
        print("solution found", startState)
        print(startState)
    que = [Node(startState, None, None)] #setup the queue to have the nodes waiting in line to get checked
    visited = [] #A list to contain nodes we have already seen
    while que:
        parent = que.pop(0) #remove and check the state at the front of the que
        for child in findPossibleStates(parent):
            if child.state == goalState: #check if the child matches goal state
                return print("Solution Found with BFS",child.state, "Path cost ",actionCost),
            if child.state not in visited: # if not we add the child to the list of failures and add the child's children to the back of queue
                visited.append(child.state)
                que.append(child)
                #print(child.state)
                actionCost += 1

def depthFirst(startState, goalState):
    actionCost = 0  # an int for counting how many steps are taken to find solution
    if startState == goalState: #Check if we already have a solution, unlikely but good to have
        print("solution found", startState)
        print(startState)
    stack = [Node(startState, None, None)] #setup the stack we will be saving our states in
    visited = [] #A list to contain nodes we have already seen
    while stack:
        parent = stack.pop() #remove and check the state at the top of the stack
        for child in findPossibleStates(parent):
            if child.state == goalState: #check if the child matches goal state
                return print("Solution Found with DFS",child.state, "Path cost ",actionCost),
            if child.state not in visited: # if not we add the child to the list of failures and add the child's children to the top of the stack
                visited.append(child.state)
                stack.append(child)
                #print(child.state)
                actionCost += 1



startState = [2, 8, 3, 1, 6, 4, 7, 0, 5]
goalState  = [1, 2, 3, 8, 0, 4, 7, 6, 5]
#uncomment the line below to start with a random startState
#random.shuffle(startState)

#uncomment the line below to search for a random goalState, if anyone wants to do that for some reason
#random.shuffle(goalState)

"""
If you Run the code with the preset start and goal states, BFS will find a solution after checking 34 nodes
If you Run the code with the preset start and goal states, DFS will find a solution after checking 6268 nodes
"""
print("Initial State",startState)
breadthFirst(startState, goalState)
depthFirst(startState, goalState)

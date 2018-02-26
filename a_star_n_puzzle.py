import heapq
import numpy as np

def flatten(board):
    # if it's nested lists, flatten them. I do this with list comprehension taking each tile at a time from each sublist
    if type(board[1])==list:
        board = [item for sublist in board for item in sublist] 
    # else, it should be a list of ints or floats
    elif type(board[1])==int or type(board[1])==float: 
        board = board
    # if it's neither, it's a wrong input and will raise an error.
    else:
        raise ValueError("Class 'PuzzleNode' got values that are not a sublist of ints nor a flat list of ints.")
    return board

"""
Class: PuzzleNode
Purpose: Object for each puzzle board created during search
Arg: None
Class Functions
    __hash__(): return a hash value for the puzzle board to id the puzzle
    
    __str__(): return a matrix representation of the puzzle board in string format
    
    __eq__(others): return True if another PuzzleNode object is identical
    
    get_moves(): return PuzzleNodes object that are the possible moves 
                    of a puzzle
    
    list_of_list(): transform the 1d array representation of the puzzle
                    into a multi-d array representation
"""
class PuzzleNode():
    def __init__(self, n, values, cost, parent, heuristic):
        
        #parent of the candidate puzzle
        self.parent = parent
        
        #dimension of the puzzle
        self.n = n
        #value of the initial puzzle pieces, stored as a 1d array
        self.tiles = flatten(values)
        self.tiles=values
        
        #Cost for A* search: g+h
        #g = stepcost; every move in the puzzle incur the same cost
        #h = heurcost; cost corresponding to the heuristic used in the method
        #Cost of step = totalcost; total cost for each candidate move
        """self.stepcost = cost
        self.heurcost = heuristic(self.tiles)
        self.totalcost = self.stepcost + self.heurcost"""
        
        # To reconstruct the optimal solution, we need to store all the steps 
        # To easily access each of the puzzles we have gone through, we store the hash value associated with each puzzle
        self.puzzleid = hash(tuple(self.tiles))
    
    #Hash the puzzle to have the puzzleid, or just return the puzzleid if there is one
    def __hash__(self):
        if seld.puzzleid is None:
            self.puzzleid = hash(tuple(self.tiles))
        return self.puzzleid
    
    #Print out a grid of the board state
    def __str__(self): 
        #To print a grid, it is easier to convert the 1d board array to text first
        strings_list = [str(x) for x in self.tiles]
        #Create n rows and n columns
        rows = [" ".join(strings_list[i:i + self.n]) for i in xrange(0, self.n**2, self.n)]
        #Break the rows into different lines
        return "\n".join(rows)
    
    # For checking if 2 candidate puzzles are equal
    def __eq__(self, other):
        return self.tiles == other.tiles
    
    #For getting possible moves from the current state
    def get_moves(self):
        #get the index of where the 0 is
        zeroPos = self.tiles.index(0)
        n = self.n 

        #Swap appropriate tiles with the 0 tile
        def swap(zeroPos,move,n):
            temp = list(self.tiles)
            swapPos = zeroPos + move
            #Evaluating edge cases
            if zeroPos%n == n-1 and move == 1:
                return
            elif zeroPos%n == 0 and move == -1:
                return
            elif zeroPos - n < n and move == -n:
                return
            elif zeroPos/n == n-1 and move == n:
                return
            elif swapPos < 0:
                return
            #Swap tiles and create new PuzzleNode object to store the new board
            else:
                temp[zeroPos],temp[swapPos] = temp[swapPos],temp[zeroPos]
                result = PuzzleNode(self.n,temp,0,self.puzzleid,None)
            return result
        
        #Generate at most 4 candidate boards from the current board
        yield swap(zeroPos,1,n)
        yield swap(zeroPos,-1,n)
        yield swap(zeroPos,n,n)
        yield swap(zeroPos,-n,n)
    
    #transform the tiles again from 1d array to list of lists
    def list_of_list(self):
        print [self.tiles[i:i+self.n] for i in xrange(0, self.n**2, self.n)]


"""
Function: solvePuzzle
"""
def solvePuzzle (n, state, heuristic_id, prnt=False):
    
    #Retrieve current state of the puzzle board after verification
    err, reason, initial_state = verify_input(state,n)
    
    queue = [] #priority queue to determine the least costly node to search
    total_cost = {} #total cost of the shortest path
    heuristic_cost = {} #cache of previous heuristic cost of boards
    visited = {} #the puzzle boards expanded and searched
    steps_to_sol = [] #detailed steps towards solution
    frontierSize = 0
    
    
    #Defining current state and goal state
    start = PuzzleNode(n, initial_state, 0, None, heuristic)
    goal = PuzzleNode(n, range(n**2),100,None,heuristic)
    
    #Initializing heap and total cost
    heapq.heappush(queue,(0,start))
    total_cost[start] = 0
    
    
    for steps in xrange(1000):
        #Select the least costly node to expand using priority queue
        cost, current = heapq.heappop(queue)
        current_cost = total_cost[current]

        #When the current board matches with the goal board
        if current.tiles == goal.tiles:
            print "Puzzle Solved!\n"

            if prnt:
                print "Initial Puzzle Board:\n"
                print "{}\n".format(start.__str__())
                print "Final Puzzle Board:\n"
                print "{}\n".format(current.__str__())

            return steps, frontierSize, err

        #Get all the candidates for next move based on the current board
        candidates = current.get_moves()
        #Evaluate every candidate move
        for move in candidates:
            if prnt == True:
                step_to_sol.append(move.current_state)
            #Prevent searching an already searched puzzle board
            if move not in total_cost or total_cost[move] > current_cost + 1:
                total_cost[move] = current_cost + 1
                #Add the unaccounted heuristic cost into the cache
                if move not in heuristic_cost:
                    move_list = move.list_of_list()
                    #update the total cost of the move
                    total_cost[move] += heuristic(move_list)

                #Put the searched puzzle board into the visited store
                visited[move] = move
                #Push the path back to the priority queue
                heapq.heappush(queue,(total_cost[move],move))

            #Update the frontierSize
            frontierSize = max(frontierSize,len(queue))
        
    else:
        raise Exception("Did not find a solution within 1000 steps.")

"""
Function: manhattanDistance

Purpose: One of the heuristics to solve the N-puzzle problem.
         Calculate the manhattan distance of any given board
        (the number of moves needed to transform any given board 
         to a complete board)

Arg:
    board: (list) a list-of-lists representation of the puzzle board
    n: (int) the dimension of the board
    
Return:
    manDis: (int) the total manhattan distance of a given puzzle board
    
**Auxiliary function: manhattanDistance_per_tile(tiles,i,n)
Purpose: calculate the manhattan distance of a given tile in the board
Arg:
    tiles: (int) the numeric value of the tile
    i: (int) the position of the tile (array index of the board array)
    n: (int) dimension of the given board
Return:
    steps: (int) manhattan distance of the given tile in the given puzzle
"""
def manhattanDistance(board,n):
    #Convert the board back to 1d array for easy manipulation
    tiles = flatten(board)
    manDis = 0
    #Sum the manhattanDistance of all the tiles
    for i in tiles:
        manDis += manhattanDistance_per_tile(tiles[i],i,n)
    return manDis
    
def manhattanDistance_per_tile(tiles,i,n):
    goalPos = tiles
    currentPos = i
    steps = 0
    #Perform when the tile is not at its place
    while currentPos != goalPos:
        #Shift levels when the current position of the tile is not at the same level
        if currentPos/n != goalPos/n:
            if currentPos > goalPos:
                currentPos -= n
            else:
                currentPos += n
            steps += 1
        #Move left or right depending on where the tile needs to go
        else:
            if currentPos > goalPos:
                currentPos -= 1
            else:
                currentPos += 1
            steps += 1
    return steps

"""
Function: misplaceTiles

Purpose: One of the heuristics for the N-puzzle problem. 
         Calculate the number of misplaced tiles in a given puzzle board
         
Arg:
    board: (list) a list-of-lists representation of a given puzzle board
    
Return:
    misplace: (int) number of misplaced tiles in the given puzzle board
"""
def misplacedTiles(board):
    tiles = flatten(board)
    misplace = 0
    for i in tiles:
        if tiles[i] != i:
            misplace += 1
    return misplace
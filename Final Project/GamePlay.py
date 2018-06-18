import time
from numpy import mean
from ConnectFourClass import ConnectFour
from MonteCarloClass import MonteCarloNode
import ConnectFourSolver 

#Simulation of gameplay
noOfSim = 50
originalNoOfSim = noOfSim
gameCount = 1

players = ['','NegaMax','MCTS-UCT']
mctsWin = 0.0
negaWin = 0.0
avgNegaSearchStep = []
avgNegaSearchDepth = []
avgNegaRunTime = []
avgMCTSSearchStep = []
avgMCTSSearchDepth = []
avgMCTSRunTime = []

game = ConnectFour()

while noOfSim > 0:
    currentState = [[],[],[],[],[],[],[]]
    game.state = currentState
    player = noOfSim%2+1
    currentPlayer = player

    allNegaSearchStep = []
    allNegaSearchDepth = []
    allNegaRunTime = []
    allMctsSearchStep = []
    allMctsSearchDepth = []
    allMctsRunTime = []

    while not game.terminal(currentState):
        if currentPlayer == 1:
            start_time = time.time()
            negaRunTime = 0.0
            negaNode, negaScore, negaSearchStep, negaSearchDepth = negamax(game,currentState,currentPlayer,max_depth=4)
            negaRunTime = time.time()-start_time
            negaAction = negaNode.action

            if game.legal(currentState,negaAction):
                currentState = game.update_state(currentState,negaAction,currentPlayer)
                currentPlayer = game.next_player(currentPlayer)

            allNegaSearchStep.append(negaSearchStep)
            allNegaSearchDepth.append(negaSearchDepth)
            allNegaRunTime.append(negaRunTime)

        else:
            start_time = time.time()
            mctsRunTime = 0.0
            mctsAction, mctsSearchStep, mctsSearchDepth = mcts_uct(game,currentState,currentPlayer,200)  #using the UCT variant of MCTS algorithm
            mctsRunTime = time.time()-start_time

            if game.legal(currentState,mctsAction):
                currentState = game.update_state(currentState,mctsAction,currentPlayer)
                currentPlayer = game.next_player(currentPlayer)

            allMctsSearchStep.append(mctsSearchStep)
            allMctsSearchDepth.append(mctsSearchDepth)
            allMctsRunTime.append(mctsRunTime)

    avgNegaSearchStep.append(mean(allNegaSearchStep))
    avgNegaSearchDepth.append(mean(allNegaSearchDepth))
    avgNegaRunTime.append(mean(allNegaRunTime))

    avgMCTSSearchStep.append(mean(allMctsSearchStep))
    avgMCTSSearchDepth.append(mean(allMctsSearchDepth))
    avgMCTSRunTime.append(mean(allMctsRunTime))

    outcome = game.outcome(currentState,player)
    if outcome > 0:
        print "{} won the {}-th game.".format(players[player],gameCount)
        if player == 1: negaWin += 1
        else: mctsWin += 1
    elif outcome < 0:
        if player == 1:
            print "{} won the {}-th game.".format(players[player+1],gameCount)
            mctsWin += 1
        else:
            print "{} won the {}-th game.".format(players[player-1],gameCount)
            negaWin += 1
    else:
        print "{}-th game is draw.".format(gameCount)

    gameCount += 1
    noOfSim -= 1

#Results
negaWinRatio = negaWin/originalNoOfSim
mctsWinRatio = mctsWin/originalNoOfSim
print "\n==============================================================="
print "Here are the results for the simulation"
print "                                   NegaMax   vs   MCTS-UCT"
print "Win Ratio:                          %.2f            %.2f" %(negaWinRatio,mctsWinRatio)
print "Runtime (sec/move):                %.3f           %.3f" %(mean(avgNegaRunTime),mean(avgMCTSRunTime))
print "Average Search Step (per move):    %.3f        %.3f" %(mean(avgNegaSearchStep),mean(avgMCTSSearchStep))
print "Average Search Depth (per move):   %.3f         %.3f" %(mean(avgNegaSearchDepth),mean(avgMCTSSearchDepth))
print "\n===============================================================\n"

#actual gameplay
game = ConnectFour()
currentState = game.state
player = 1

print "There are two variation of AI algorithm you can play with:"
print "Negamax (negamax): A simpler variation of Minimax algorithm"
print "UCT Variant of MCTS (monteuct): MCTS with the UCT search-weighting function"
selection = str(raw_input("\nWhich AI algorithm do you want to play against (negamax,monteuct): "))

print "\nYou are playing with an AI agent that uses {}".format(selection)
print "\n====================================================\n"

currentPlayer = player
while not game.terminal(currentState):
    if currentPlayer == 1:
        humanAction = int(raw_input("Choose a column: "))
        if game.legal(currentState,humanAction):
            currentState = game.update_state(currentState,humanAction,currentPlayer)
            currentPlayer = game.next_player(currentPlayer)
            print "You played column {}".format(humanAction)
    else:
        if selection == "monteuct":
            computerAction,searchStep,searchDepth = mcts_uct(game,currentState,currentPlayer,2000)  #using the UCT variant of MCTS algorithm
        elif selection == "negamax":
            computerNode, computerScore,searchStep,searchDepth = negamax(game,currentState,currentPlayer,max_depth=4)
            computerAction = computerNode.action
        else:
            raise ValueError("Invalid Choice of the AI algorithm")

        if game.legal(currentState,computerAction):
            currentState = game.update_state(currentState,computerAction,currentPlayer)
            currentPlayer = game.next_player(currentPlayer)
            print "The computer played column {}".format(computerAction)

    currentBoard = game.pretty_state(currentState)
    print currentBoard

outcome = game.outcome(currentState,player)
if outcome > 0:
    print "You won!"
elif outcome < 0:
    print "You lose!"
else:
    print "Draw!"

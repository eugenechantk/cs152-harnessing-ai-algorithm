#Implemented from my past assignment
#Use to flatten the state of the 2d board so to allow hashing
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

#returns the best node (and best score) for a given state
def negamax(game,state,player,depth=0,max_depth=4,parent=None,action=None,s_steps=0,s_depth=0):
    current = MonteCarloNode(state,action,player,game,parent,max_depth)

    search_step = s_steps
    search_depth = s_depth

    search_step += 1

    if current in game.evaluated:
        return (current, current.nega_value,search_step,search_depth)

    if depth == current.max_depth:
        score = current.game.evaluate(current.state,current.player)
        game.evaluated[current] = score
        return (current, score,search_step,search_depth)

    best_score = float('-inf')
    best_node = None

    for nextAction in game.actions(current.state):
        nextState = game.update_state(current.state,nextAction,current.player)

        if game.terminal(nextState):
            outcome = game.outcome(nextState,player)
            if outcome == game.VALUE_WIN:
                current.nega_value = 99999
            elif outcome == game.VALUE_LOSE:
                current.nega_value = -99999
            else:
                current.nega_value = 0
            best_subscore = current.nega_value
            nextPlayer = game.next_player(current.player)
            #create MonteCarloNode to retrieve the action at this level
            best_subnode = MonteCarloNode(nextState,nextAction,nextPlayer,game,current,max_depth)

        else:
            nextPlayer = game.next_player(current.player)
            newDepth = depth + 1

            (best_subnode, best_subscore, search_step, search_depth) = negamax(game,nextState,nextPlayer,newDepth,max_depth,current,nextAction,search_step,search_depth)
            best_subscore *= -1

        if best_subscore > best_score:
            best_score = best_subscore
            best_node = best_subnode

    if best_node is None:
        best_score = game.evaluate(current.state,player)

    search_depth += 1

    game.evaluated[current] = best_score

    return (best_node, best_score, search_step, search_depth)

#Monte Carlo Tree Search (UCT-variant)
def mcts_uct(game,state,player,budget,c=(1/sqrt(2))):
    root = MonteCarloNode(state,None,player,cur_game=game,parent=None)
    computerWin = 0.0
    originalBudget = budget

    search_step = max_search_depth = 0

    while budget:
        child = root
        child = child._tree_policy()
        search_step += 1
        reward = child._default_policy(player)
        search_depth = child._backup(reward,budget)
        if search_depth > max_search_depth:
            max_search_depth = search_depth
        budget-=1

    bestChild = root._best_child(c)
    return bestChild.action, search_step, max_search_depth

from math import sqrt, log
import random

class MonteCarloNode():

    def __init__(self,state,action,player,cur_game=None,parent=None,max_depth=None):
        self.game = game or parent.game

        #About the parents and children of the node
        self.parent = parent
        self.children = dict.fromkeys(self.game.actions(state))

        #About the move of the node
        self.state = state
        self.action = action

        #About the player and the reward of the node
        self.player = player
        self.visit = 0.0
        self.value = 0.0
        self.weight = 0.0

        #For Negamax algorithm implementation
        self.nega_value = 0
        self.max_depth = max_depth
        self.flatten_state = flatten(self.state)
        self.stateId = hash(tuple(self.flatten_state))

    def __hash__(self):
        if self.stateId is None:
            self.stateId = hash(tuple(self.flatten_state))
        return self.stateId

    def _tree_policy(self):
        bestNode = self
        while not bestNode.game.terminal(self.state):
            if not bestNode._fully_expanded():
                return bestNode._expand()
            else:
                bestNode = bestNode._best_child()
        return bestNode

    def _expand(self):
        try:
            expAction = self.children.keys()[self.children.values().index(None)]
        except ValueError:
            raise Exception('Node is already fully expanded')

        expState = self.game.update_state(self.state,expAction,self.player)
        expPlayer = self.game.next_player(self.player)

        child = MonteCarloNode(expState,expAction,expPlayer,self.game,self)
        self.children[expAction] = child
        return child

    def _fully_expanded(self):
        return not None in self.children.values()

    def _weight(self):
        if self.visit == 0:
            return 0.0
        else:
            return self.value/self.visit

    def _default_policy(self,player):
        game = self.game
        curState = self.state
        curPlayer = self.player
        while not game.terminal(curState):
            curAction = random.choice(game.actions(curState))
            curState = game.update_state(curState,curAction,curPlayer)
            curPlayer = game.next_player(curPlayer)
        reward = game.outcome(curState,player)
        return reward

    def _backup(self,reward,budget,pntlevel=0):
        backupNode = self
        search_depth = 1
        while not backupNode is None:
            backupNode.value += reward
            backupNode.visit += 1
            search_depth += 1
            backupNode = backupNode.parent

            if pntlevel != 0:
                if budget % 100 == 0:
                    print backupNode

        return search_depth

    def _best_child(self,c=1/sqrt(2)):
        return max(self.children.values(), key=lambda x: x._search_weight(sqrt(c)))

    def _search_weight(self, c):
        return self._weight() + c * sqrt(2 * log(self.parent.visit) / self.visit)

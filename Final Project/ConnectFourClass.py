class ConnectFour():

    ROW = 6
    COLUMN = 7
    INITIAL_STATE = [[],] * COLUMN
    PLAYERS = (1,2)
    GOAL = 4
    VALUE_WIN = 1
    VALUE_LOSE = -1
    VALUE_DRAW = 0

    #For Negamax algorithm implementation
    STREAK_WEIGHT = [1, 8, 128, 99999]
    evaluated = {}

    def __init__(self,row=ROW,column=COLUMN,state=INITIAL_STATE,player=PLAYERS,goal=GOAL):
        self.row = row
        self.column = column
        self.state = state
        self.player = player
        self.goal = goal

    def legal(self,state,action):
        if len(self.state[action]) >= self.row:
            raise Exception("Invalid action: columnn is full!")
        else:
            return len(self.state[action]) < self.row

    def actions(self, state):
        return [i for i in xrange(len(state)) if self.legal(state, i)]

    def update_state(self, state, action, player):
        if not self.legal(state, action):
            raise Exception('Illegal action')
        newstate = []
        for index, column in enumerate(state):
            if index == action:
                newstate.append(column + [player])
            else:
                newstate.append(column)
        #newstate[len(state)-1] = player
        return newstate

    def streak(self,state,player,start,delta,length=0):
        row, column = start
        if row < 0 or column < 0:
            return False

        try:
            piece = state[column][row]
        except IndexError:
            return False

        if piece != player:
            return False

        # Current slot is owned by the player
        length += 1
        if length == self.goal: # Streak is already long enough
            return True
        # Continue searching,
        drow, dcolumn = delta

        return self.streak(state,player,(row + drow, column + dcolumn),delta,length)


    def outcome(self, state, player):
        for col, column in enumerate(state):
            for row, marker in enumerate(column):
                if any((
                    self.streak(state, marker, (row, col), (1, 0)),  #check upwards
                    self.streak(state, marker, (row, col), (0, 1)),  #check rightward
                    self.streak(state, marker, (row, col), (1, 1)),  #check right diagonal
                    self.streak(state, marker, (row, col), (1, -1)), #check left diagonal
                )):
                    # A winner was found
                    if marker == player:
                        return self.VALUE_WIN
                    else:
                        return self.VALUE_LOSE
        # No winner was found
        return self.VALUE_DRAW

    def terminal(self, state):
        if all([len(column) == self.row for column in state]):  #when all columns are full
            return True
        if self.outcome(state, self.player[0]) != self.VALUE_DRAW:  #when there is a winner
            return True
        return False  #the board still have space and the game is still on

    def next_player(self, player):
        if player not in self.player:
            raise Exception('Invalid player')
        index = self.player.index(player)
        if index < 1:
            return self.player[index + 1]
        else:
            return self.player[0]

    def pretty_state(self, state, escape=False):
        output = ''
        for j in range(self.column):
            output += ' ' + str(j)
        output += ' '
        if escape:
            output += '\\n'
        else:
            output += '\n'
        #boardState = state[1:self.column-1]
        i = self.row - 1
        while i >= 0:
            for column in state:
                if len(column) > i:
                    output += '|' + str(column[i])
                else:
                    output += '| '
            output += '|'
            if escape:
                output += '\\n'
            else:
                output += '\n'
            i -= 1
        return output


    #For Negamax algorithm implementation
    def streak_eval(self,state,player,start,delta,length=0,max_length = 0):
        row, column = start
        if row < 0 or column < 0:
            return max_length

        try:
            piece = state[column][row]
        except IndexError:
            return max_length

        if piece != player:
            length = 0

        # Current slot is owned by the player
        length += 1
        if length > max_length: # if current streak is longer than the max_length
            max_length = length
        # Continue searching,
        drow, dcolumn = delta

        if row == self.row and column == self.column:
            return max_length

        return self.streak_eval(state,player,(row + drow, column + dcolumn),delta,length,max_length)

    def evaluate(self,state,player):
        curPlayer = player
        curPlayerValue = 0
        otherPlayerValue = 0

        for col, column in enumerate(state):
            for row, marker in enumerate(column):
                max_length_up = self.streak_eval(state, marker, (row, col), (1, 0))  #check upwards
                max_length_right = self.streak_eval(state, marker, (row, col), (0, 1))  #check rightward
                max_length_diaright = self.streak_eval(state, marker, (row, col), (1, 1))  #check right diagonal
                max_length_dialeft = self.streak_eval(state, marker, (row, col), (1, -1)) #check left diagonal
                if marker == curPlayer:
                    max_length = max(max_length_up,max_length_right,max_length_diaright,max_length_dialeft)
                    curPlayerValue += self.STREAK_WEIGHT[max_length-1]
                    #print "Player two value updated: max_length:{} player_2_value:{}\n".format(max_length, player_2_value)
                else:
                    max_length = max(max_length_up,max_length_right,max_length_diaright,max_length_dialeft)
                    otherPlayerValue += self.STREAK_WEIGHT[max_length-1]
                    #print "Player one value updated: max_length:{} player_1_value:{}\n".format(max_length, player_1_value)

        difference = curPlayerValue - otherPlayerValue
        return difference

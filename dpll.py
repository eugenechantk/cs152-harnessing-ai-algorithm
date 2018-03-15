from copy import deepcopy
import operator



#########################
#Create Literal Object Class
#########################
"""
Class: Literals
Purpose: Defining a literal object in our knowledge base
Class Functions:
    __str__(self):         Print the name of the literal, with the negative 
                           sign representing negated literals
    __repr__(self):        Official string representation
    __neg__(self):         Create another negate literal object
    __eq__(self):          When comparing literals, it disregards the sign of 
                           the literal
    __hash__(self):        Hash the literal object so to be able to retrieve
    __getitem__(self,item) Redirect a dictionary to return the literal object
"""
class Literal:
    def __init__(self,name='',sign=True):
        self.name = name
        self.sign = sign
        
    def __str__(self):
        if self.sign:
            return self.name
        elif self.name == 'False':
            return self.name
        else:
            return "-" + self.name
        
    def __repr__(self):
        return self.__str__()
    
    def __neg__(self):
        negLiteral = Literal(self.name)
        negLiteral.sign = False
        return negLiteral
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __getitem__(self, item):
        return self



#########################
#Unit Propagation
#########################
"""
Function: Simplify
Purpose: Using unit propagation to simplify the clauses we are evaluating
Arg:
    clauses: (list of sets) the clauses we are evaluating
    symbol: (Literal object) the unit clause/literal we are propagating
    sign: (bool) the sign of the unit clause/literal we are propagating
Return:
    simplifiedClauses: (list of sets) the simplified clauses after unit
                        propagation
"""
def Simplify(clauses,symbol,sign):
    simplifiedClauses = []
    
    def simplify_clause(clause):  #evaluate each clause
        newClause = set()
        if symbol in clause:  #if the unit exist in the clause
            for literal in clause:
                if literal == symbol:
                    #two cases to turn the clause to true:
                    #First case: unit is true and literal is true
                    if literal.sign == True and sign == True: 
                        newClause.clear()
                        newClause.add(T)
                        break
                    #Second case: unit is false and literal is false
                    elif literal.sign == False and sign == False:
                        newClause.clear()
                        newClause.add(T)
                        break
                    else:
                        continue
                else:
                    newClause.add(literal)  #put the remaining literal into the new clause
            if len(newClause) == 0:
                #if it is unit clause, and does not satisfy the first two cases
                #that means the clause is automatically falsified
                newClause.add(Fal)
            return newClause
        else:
            newClause = clause
            return newClause
    
    for clause in clauses:
        sim_clause = simplify_clause(clause)
        simplifiedClauses.append(sim_clause)  #add the new, simplified clauses
    
    return simplifiedClauses  #return all the simplified clauses



#############################
#Different Heuristics for DPLL
#First heuristic: Degree Heuristic
#############################
"""
Function: sort_symbol
Purpose: Create a list of symbols, sorted in descending order, 
         based on the number of occurence in the knowledge base
Arg:
    KB: (list of sets) the clauses in the initial knowledge base
Return:
    sorted_symbols: (list) symbols in descending order of number of occurences 
                    in the knowledge base
"""
def sort_symbols(KB):
    symbols = {}
    for clause in KB:
        for literal in clause:
            if literal not in symbols:
                symbols[literal] = 1
            else:
                symbols[literal] += 1

    sorted_symbols = sorted(symbols.items(), key=operator.itemgetter(1), reverse=True)
    return [sorted_symbols[i][0] for i in xrange(len(sorted_symbols))]

"""
Function: sort_symbol_in_DPLL
Purpose: Create a list of symbols, sorted in descending order, 
         given the symbols available at each node of the DPLL backchaining tree
Arg:
    symbols: (list) the symbols available to evaluate for the node
    clauses: (list of sets) the clauses evaluating for the node
Return:
    sorted_symbols: (list) symbols in descending order of number of occurences 
                    in the clauses we are evaluating
"""
def sort_symbol_in_DPLL(symbols,clauses):
    num_of_symbols = {}
    for symbol in symbols:
        for clause in clauses:
            for literal in clause:
                if literal == symbol:
                    if literal not in num_of_symbols:
                        num_of_symbols[symbol] = 1
                    else:
                        num_of_symbols[symbol] += 1
    sorted_symbols = sorted(num_of_symbols.items(), key=operator.itemgetter(1), reverse=True)
    return [sorted_symbols[i][0] for i in xrange(len(sorted_symbols))]



#############################
#Second heuristic: Pure Symbol Heuristic
#############################
"""
Function: get_pure_symbol(clauses,symbols)
Purpose: Return the first symbol in the clauses with consistent sign 
         (either postive or negative)
Arg:
    clauses: (list of sets) the clauses we are evaluating
    symbols: (ordered list) list of symbols in descending order of the 
             number of occurence in the clauses evaluating
Return:
    symbol: (Literal object) the pure symbol given clauses
    sign: (bool) True(for original literal) and False(for negated literals)
"""
def get_pure_symbol(clauses,symbols):
    
    
    def check_pure(symbol):   #checking whether each symbol is pure
        pure_symbol= None
        for clause in clauses:
            if symbol in clause:   #if the symbol searching is in the clause
                for literal in clause:   #look through the literals in the clause
                    if literal == symbol:   #if the literal is the symbol
                        if pure_symbol is None:   #set literal as pure symbol for first occurence
                            pure_symbol = literal
                        else:
                            if literal.sign != pure_symbol.sign:  #clear pure symbol if the signs of either two literals are not the same
                                return None, None
        if pure_symbol is not None:
            return pure_symbol, pure_symbol.sign  #return the pure symbol and sign if exist
        else:
            return None, None  #if pure symbol does not exist, return nothing
        
    for symbol in symbols:  #looping through all the symbols
        (pure_symbol, pure_sign) = check_pure(symbol)
        if pure_symbol is not None:  #if there is a pure symbol already, return the pure symbol
            return symbol, pure_sign
    
    return None, None



#############################
#Third heuristic: Unit Clause Heuristic
#############################
"""
Function: get_unit_clause
Purpose: Return the first unit clause given clauses, and the sign 
         of the literal in the unit clause
Arg: 
    clauses: (list of sets) clauses currently evaluating
Return:
    literal: (Literal symbol) The literal in the unit clause
    sign: (bool) The sign of the literal in the unit clause
"""
def get_unit_clause(clauses):
    unit_clause = None  #initialize the unit_clause
    unit_sign = None
    for clause in clauses:  #search all the clauses
        if len(clause) == 1 and T not in clause and Fal not in clause: 
            for literal in clause: #if there is unit clause, and it is not T or F, return it
                return literal, literal.sign
        
    return None, None #if there is no unit clause, return nothing



#############################
#DPLL Algorithm Implementation
#############################
"""
Function: DPLLSatisfiable
Purpose: Determine whether a knowledge base is satisfiable by finding a model
         where all the clauses in the KB are true
Arg:
    KB: (list of sets) the clauses in the knowledge base
Return:
    A model and the corresponding value of the literals if the KB is satisfiable
    Return False if the knowledge base is not satisfiable
"""
def DPLLSatisfiable(KB):
    
    def merge_two_dicts(x, y):
        z = x.copy()
        z.update(y)
        return z
    
    """
    **SUB-FUNCTION in DPLLSatisfiable**
    Function: DPLL
    Purpose: Determine, at each node of the DPLL backchaining tree, where the KB is 
             satisfiable, given some literals and their true values
    Arg:
        clauses: (list of sets) the clauses available at the node
        symbols: (list) the symbols available at the node
        unit_prop_symbol: (Literal object) the symbol used to propagate at this node
        unit_prop_sign: (bool) the sign of the symbol used to propagate at this node
    Return:
        bool: True if the KB is satisfiable at the node; False if it is not satisfiable
    """
    def DPLL(clauses,symbols,model, unit_prop_symbol=None, unit_prop_sign=None):
        #initialize the final, satisfiable model
        global sat_model
        sat_model = {}
        
        #unit propagation to simplify the clauses
        if unit_prop_symbol is not None:
            clauses = Simplify(clauses,unit_prop_symbol,unit_prop_sign)
        
        """
        Status of each DPLL recursive call (for debugging)    
        print "==================================="
        print "These are the clauses: {}\n".format(clauses)
        print "These are the symbols: {} ({})\n".format(symbols,len(symbols))
        print "This is the current model: {}\n".format(model)
        print "This is the unit propagating: {} {}\n".format(unit_prop_symbol,unit_prop_sign)
        """
        
        #apply degree heuristics to the available symbols in the node
        symbols = sort_symbol_in_DPLL(symbols,clauses)
        
        #If all the clauses are deemed true, set the current model as
        #the satisfiable model
        if all([T in clause for clause in clauses]):
            sat_model = model
            return True
        
        #if there is any clause that is deemed false, the current model is 
        #not satisfiable; return False
        if any([Fal in clause for clause in clauses]):
            return False
        
        
        if len(symbols) != 0:  #if there are still symbols to evaluate in this node
            
            #applying pure symbol heuristic
            pure_symbol, pure_sign = get_pure_symbol(clauses,symbols)  #find pure symbol
            if pure_symbol is not None:  #if there is pure symbol, go down on that path
                unit_prop_symbol = pure_symbol  #set the unit to propagate next as the pure symbol
                unit_prop_sign = pure_sign
                symbols.remove(pure_symbol)
                model.update({pure_symbol: pure_sign}) #add the pure symbol to current model
                clause_after_pure = deepcopy(clauses)  #deep copy the clauses to parse into the next level
                symbols_after_pure = deepcopy(symbols) #deep copy the symbols to parse into the next level
                return DPLL(clause_after_pure,symbols_after_pure,model,pure_symbol,pure_sign)
            
            
            #applying unit clause heuristic
            unit_symbol, unit_sign = get_unit_clause(clauses)  #find the unit clause
            if unit_symbol is not None:
                unit_prop_symbol = unit_symbol #set the unit to propagate next as the same literal and sign as the unit clause
                unit_prop_sign = unit_sign     #same sign and literal will make the unit clause true
                symbols.remove(unit_symbol)
                model.update({unit_symbol: unit_sign}) #add the unit symbol to current model
                clause_after_unit = deepcopy(clauses)  #deep copy the clauses to parse into the next level
                symbols_after_unit = deepcopy(symbols) #deep copy the symbols to parse into the next level
                return DPLL(clause_after_unit,symbols_after_unit,model,unit_symbol,unit_sign)
            
            #apply degree heuristic last
            p = symbols.pop(0)  #take the most occured literal out
            p_true = {p:True}  
            p_false = {p:False}
            p_true = merge_two_dicts(p_true,model)  #create two models: p = True, p = False
            p_false = merge_two_dicts(p_false,model)
            
            clause_after_pop = deepcopy(clauses)  #deep copy the clauses to parse into the next level
            symbols_after_pop_true = deepcopy(symbols)  #deep copy the clauses to parse into the next level
            symbols_after_pop_false = deepcopy(symbols) #deep copy the clauses to parse into the next level
            
            #evaluate the true path before the false path
            return DPLL(clause_after_pop,symbols_after_pop_true,p_true,p,True) or DPLL(clause_after_pop,symbols_after_pop_false,p_false,p,False)
    
    #apply degree heuristic before using DPLL
    symbols = sort_symbols(KB)
    symbols_for_use = deepcopy(symbols)
    
    #run DPLL to a find satisfiable model
    satisfy = DPLL(KB,symbols_for_use,{}) 
    
    #if there is a satisfiable model, print the model
    if satisfy:
        print "The Knowledge Base is Satisfiable!"
        print "This is a satisfiable model:"
        for symbol in symbols:
            if symbol in sat_model:
                print str(symbol.name) + ": " + str(sat_model[symbol])
            else:
                print str(symbol.name) + ": Free"


#############################
#SAT solving for sample knowledge base
#############################
A = Literal('A')
B = Literal('B')
C = Literal('C')
D = Literal('D')
E = Literal('E')
F = Literal('F')
T = Literal('True')
Fal = Literal('False',False)

KB = [{-A, B, E}, {-B, A}, {-E, A}, {-E, D}, 
      {-C, -F, -B}, {-E, B}, {-B, F}, {-B, C}]

DPLLSatisfiable(KB)
from typing import final
from regex import regexToTree

class Automata:
   
    def __init__(self, states = None, symbols = None, start = None, acceptance = None, transitions = None):
       
        if (states is None or symbols is None or start is None or acceptance is None or transitions is None):
            raise ValueError("Por favor ingresa los valores correctos")
        elif (len(states) < 0 or len(symbols) < 0 or len(start) < 0 or len(acceptance) < 0 or len(transitions) < 0):
            raise ValueError("Por favor ingresa los valores correctos")

        self.states = states
        self.symbols = symbols
        self.start = start
        self.acceptance = acceptance
        self.transitions = transitions
        self.AFD = []

        self.createMatrix()
        self.toAFD()

    def createMatrix(self):
        self.matrix = [[[0 for _ in range(len(self.symbols))] for _ in range(len(self.states))] for _ in range(len(self.states))]

        for _ in range(len(self.transitions)):
            self.matrix[self.states.index(self.transitions[_][0])][self.states.index(self.transitions[_][2])][self.symbols.index(self.transitions[_][1])] = self.transitions[_][1]

    def find3scope(self,state, transitions = []):
        #print(state,transitions)
        if type(state) != list:
            #print(state not in transitions)
            if state not in transitions:
                #print("Asd")
                transitions.append(state)
                for _ in self.transitions:
                    if _[0] == state and _[1] == "&":
                        transitions = self.find3scope(_[2], transitions=transitions)
        else:
            for x in state:
                if x not in transitions:
                    transitions.append(x)
                for _ in self.transitions:
                    if _[0] == x and _[1] == "&":
                        if _[2] not in transitions:
                            transitions = self.find3scope(_[2], transitions=transitions)
        return transitions

    def getState(self, state = [], symbol = None):
        if state == []:
            return []

        if state == [None]:
            return None

        if symbol == None:
            raise ValueError("Ha ocurrido un problema al momento de obtener el AFD")

        newState = []

        for _ in state:
            res = self.transitionTable[self.states.index(_)][self.symbols.index(symbol)]
            if res is not None:
                if type(res) is list:
                    for i in res:
                        if i not in newState:
                            newState += i
                else:
                    newState += self.transitionTable[self.states.index(_)][self.symbols.index(symbol)]

        if len(newState)>1:
            return newState
        elif len(newState) == 1:
            return newState[0]
        else:
            return None


    def defineAFD(self):
        start = [self.start if type(self.start) == list else [self.start],[_ for _ in self.transitionTable[0]]]

        self.AFD.append(start)

        actualIndex = 0
        while True:
            actualState = self.AFD[actualIndex][1]
            for _ in range(len(self.symbols)):
                actualSymbol = actualState[_]


                itsOnAFD = False
                
                for afdStatus in self.AFD:
                    if type(actualSymbol) is list and actualSymbol == afdStatus[0]:
                        itsOnAFD = True
                    elif type(actualSymbol) != list and [actualSymbol] == afdStatus[0]:
                        itsOnAFD = True

                if actualSymbol == None:
                    continue

                elif itsOnAFD == False:
                    newState = [actualSymbol if type(actualSymbol) == list else [actualSymbol],[self.getState(actualSymbol,x) for x in self.symbols]]
                    self.AFD.append(newState)
            actualIndex += 1
            notFound = False
            for _ in self.AFD:
                for x in _[1]:
                    if type(x) != list: x = [x]
                    if x != [None] and x not in [y[0] for y in self.AFD]:
                        notFound = True
            
            if notFound == False:
                break
                        


    def toAFD(self):
        self.transitionTable = [[None for _ in range(len(self.symbols))] for _ in range(len(self.states))]

        for _ in range(len(self.transitions)):

            startStatus = self.transitions[_][0]
            transition = self.transitions[_][1]
            endStatus = self.transitions[_][2]

            if transition == "&":
                #print(endStatus)
                #print("empieza")
                #print(self.find3scope(endStatus))
                endStatus = self.find3scope(endStatus, transitions=[])

            #print(endStatus)
            if type(endStatus) is list:
                    endStatus = sorted(endStatus)

            symbolIndex = self.symbols.index(transition)
            statusIndex = self.states.index(startStatus)
            if self.transitionTable[statusIndex][symbolIndex] is None:
                self.transitionTable[statusIndex][symbolIndex] = endStatus
            else:
                if type(endStatus) is list:
                    for i in endStatus:
                        if i not in self.transitionTable[statusIndex][symbolIndex]:
                            self.transitionTable[statusIndex][symbolIndex] += endStatus
                else:
                    self.transitionTable[statusIndex][symbolIndex] += endStatus
                    
        #print(self.transitionTable)
        self.defineAFD()


    def setMaker(self, dict):

        statesSets, u_vals = [], []
        for i in range(len(list(dict.items()))):
            sT = list(dict.items())[i] # sT => Tuple of state and its transitions
            statesSets.append(list(sT))
            u_vals.append(list(sT[1]))

        # r_vals => repeated values
        # u_vals => unique values (r_vals)
        r_vals = list(set([tuple(t) for t in u_vals]))
        r_vals = [list(t) for t in r_vals]

        result = []
        for value in r_vals:
            new_group = [lst[0] for lst in statesSets if lst[1] == value and len(lst[1]) > 1]
            if len(new_group) > 0:
                result.append(new_group)
        
        return result
    

    def grouping(self, subGroups, nonAccepting, symbols, transitions): 

        newGroups = []
        states = [j for i in nonAccepting for j in i]

        dict = {key: [] for key in states}

        for group in subGroups:
            if len(group) == 1: continue
            for indx in range(len(group)):
                for sym in symbols:
                    for t in transitions:
                        if group[indx] == t[0] and sym == t[1]:
                            if t[2] in group and group[indx] in dict.keys(): 
                                dict[group[indx]] += [subGroups.index(group)]
                            else:
                                for grp in subGroups: 
                                    if t[2] in grp and group[indx] in dict.keys():
                                        dict[group[indx]] += [subGroups.index(grp)]
        
        for subSet in self.setMaker(dict):
            newGroups.append(subSet)

        for group in subGroups:
            for state in group: 
                if state not in [state for group in newGroups for state in group]:
                    newGroups.append(group)        
        
        return newGroups


    def partition(self):
        #Start with initial partition accepting and non-accepting states
        accepting = self.acceptance
        nonAccepting = [i for i in self.states if i not in accepting]

        #Making subsets
        subSets = [accepting, nonAccepting]

        bandera = True
        while bandera:
            prevGroups =  subSets
            prevSyms = nonAccepting
            subSets = self.grouping(subSets, prevSyms, self.symbols, self.transitions)

            if sorted(prevGroups) == sorted(subSets): 
                bandera = False
        
        newSD = {key: [] for key in range(len(subSets))}

        for indx in range(len(subSets)):
            newSD[indx] += subSets[indx]

        for indx in range(len(newSD.keys())):
            newSD[chr(ord(self.states[-1])+indx+1)] = newSD.pop(indx)

        return newSD   

    def writeTxt(self, fileName, states, symbols, start, accepting, transitions, type, dict={}):
        f= open(fileName,"w+")
        f.write("ESTADOS = " + str(states) + '\n')
        f.write("SIMBOLOS = " + str(symbols) + '\n')
        f.write("INICIO = " + str(start) + '\n')
        f.write("ACEPTACION = " + str(accepting) + '\n')
        f.write("TRANSICIONES = " + str(transitions) + '\n')

        if type == 'mini':
            f.write("NUEVA REPRESENTACION DE ESTADOS = " + str(dict) + '\n')

        f.close()


    def minimizeAFD(self, statesD):
        # Replacing states in list by new states
        newStates = [] # Creating new states list
        for k, v in statesD.items():
            newStates.append(k)

        # Replacing by new start state
        newStart = [] # Creating new start list
        for k, v in statesD.items():
            if self.start[0] in v:
                newStart.append(k)

        # Creating new aceptance list
        newAcceptance = []
        for element in self.acceptance:
            newAcceptance.append(element)

        # Replacing new acceptance states
        for k, v in statesD.items():
            for indx in range(len(newAcceptance)):
                if newAcceptance[indx] in v:
                    newAcceptance[indx] = k 
        newAcceptance = list(dict.fromkeys(newAcceptance)) # In case elements are duplicated

        # Creating new transition list
        newTransitions = []
        for element in self.transitions:
            newTransitions.append(element)

        # Converting lists to tuples
        cList = [list(i) for i in newTransitions]

        # Replacing new states in transitions list
        for transition in cList:
            for k, v in statesD.items():
                if transition[0] in v:
                    transition[0] = k
                if transition[2] in v:
                    transition[2] = k

        # Removing duplicates
        noDuplicatesList = sorted(set(tuple(l) for l in cList))
        newTransitions = noDuplicatesList

        self.writeTxt('respuestas/Minimizacion_AFD.txt', newStates, self.symbols, newStart, newAcceptance, newTransitions, 'mini', statesD)

    def fromRegeex(regex):

        return 2

# x = Automata(states=["0","1","2","3","4","5","6","7"], symbols=["a","b","&"], start=["0"], acceptance=["5","7"], transitions=[("0","&","1"), ("0","&","4"), ("1","a","2"), ("1","&","3"), ("2","a","3"), ("3","&","7"), ("7","&","0"), ("4","b","5"), ("4","&","6"), ("5","b","6"), ("6","&","7")])
# y = Automata(states=["A","B","C","D","E"], symbols=["a","b"], start=["A"], acceptance=["E"], transitions=[("A","a","B"), ("A","b","C"), ("B","a","B"), ("B","b","D"), ("C","a","B"), ("C","b","C"), ("D","a","B"), ("D","b","E"), ("E","a","B"), ("E","b","C")])
# z = Automata(states=["A","B","C","D","E","F","G","H"], symbols=["0","1"], start=["A"], acceptance=["C"], transitions=[("A","0","B"), ("A","1","F"), ("B","0","G"), ("B","1","C"), ("C","0","A"), ("C","1","C"), ("D","0","C"), ("D","1","G"), ("E","0","H"), ("E","1","F"), ("F","0","C"), ("F","1","G"), ("G","0","G"), ("G","1","E"), ("H","0","G"), ("H","1","C")])
# k = Automata(states=["A","B","C","D","E","F","G","H"], symbols=["a","b"], start=["A"], acceptance=["C", "H"], transitions=[("A","a","B"), ("A","b","E"), ("B","a","F"), ("B","b","C"), ("C","a","D"), ("C","b","G"), ("D","a","D"), ("D","b","D"), ("E","a","B"), ("E","b","E"), ("F","a","B"), ("F","b","E"), ("G","a","D"), ("G","b","H"), ("H","a","D"), ("H","b","G")])
#
# k.minimizeAFD(k.partition())

regexToTree("a.b")
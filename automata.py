class Automata:

    def __init__(self, states=None, symbols=None, start=None, acceptance=None, transitions=None):

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

        #print(states, "states")
        #print(symbols, "symbols")
        #print(start, "start")
        # print(acceptance, "acceptance")
        #print(transitions, "transitions")

        self.createMatrix()
        #self.toAFD()


    """
    Esta funcion fue disenada para determinar el la matriz que se utilizara posteriormente para algunos calculos
    de la conversion de AFN a AFD.. Cabe mencionar que genera una matriz cubica estados x estados x simbolos
    """
    def createMatrix(self):
        self.matrix = [[[0 for _ in range(len(self.symbols))] for _ in range(len(self.states))] for _ in
                       range(len(self.states))]

        for _ in range(len(self.transitions)):
            self.matrix[self.states.index(self.transitions[_][0])][self.states.index(self.transitions[_][2])][
                self.symbols.index(self.transitions[_][1])] = self.transitions[_][1]
    

    """
    Esta funcion en otras ocasiones tambien es llamada e-closure, la cual tiene como objetivo reunir el alcance
    de todos los estados que tiene un estado con epsilon.
    """
    def find3scope(self, state, transitions=[]):
        if type(state) != list:
            if state not in transitions:
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

    """
    Esta funcion tiene como objetivo reunir todos los estados que procede dependiendo del simbolo que se elije.
    """
    def getState(self, state=[], symbol=None):
        if state == []:
            return []

        if state == [None]:
            return None

        if symbol == None:
            raise ValueError("Ha ocurrido un problema al momento de obtener el AFD")

        newState = []

        if type(state) == list:
            for _ in state:
                res = self.transitionTable[self.states.index(_)][self.symbols.index(symbol)]
                if res is not None:
                    if type(res) is list:
                        for i in res:
                            if i not in newState:
                                newState.append(i)
                    else:
                        if self.transitionTable[self.states.index(_)][self.symbols.index(symbol)] not in newState:
                            newState.append(self.transitionTable[self.states.index(_)][self.symbols.index(symbol)])
        else:
            res = self.transitionTable[self.states.index(state)][self.symbols.index(symbol)]
            if res is not None:
                if type(res) is list:
                    for i in res:
                        if i not in newState:
                            newState.append(i)
                else:
                    if self.transitionTable[self.states.index(state)][self.symbols.index(symbol)] not in newState:
                        newState.append(self.transitionTable[self.states.index(state)][self.symbols.index(symbol)])

        if len(newState) >= 1:
            return newState
        else:
            return None

    """
    En esta funcion se define el AFD, aqui se llaman a las dos funciones anteriores pues el nuevo AFD debe
    contener todos los resultados posibles

    El formato en que se almacena es el siguiente

    [  [ Estado/s de Inicio ], [ por cada simbolo se agrega una lista [ contiene todos los estados a los que transiciona con ese simbolo ], ...  ]  ]
    """
    def defineAFD(self):
        start = [self.start if type(self.start) == list else [self.start], [_ for _ in self.transitionTable[self.states.index(self.start[0])]]]

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
                    newState = [actualSymbol if type(actualSymbol) == list else [actualSymbol],
                                [self.getState(actualSymbol, x) for x in self.symbols]]
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


    """
    Los procedimientos anteriores generan muchos estados sucios por los que se debe limpiar el AFD
    """
    def cleanAFD(self):
        # Esta funcion debe limpiar el AFD resultante de las funciones para convertir de AFN a AFD
        index = -1
        if '&' in self.symbols:
            index = self.symbols.index('&')
        if index != -1:
            self.changeState(index=index)

    """
    En caso un estado x tenga como unica transicion epsilon, entonces ese epsilon toma el lugar de todos los estados donde se menciona x
    asi se reducen la cantidad de estados y se eliminan algunos problemas que pueden llegar a ocurrir.
    """
    def changeState(self, index):
        remove = []

        for x in self.AFD:
            for i in self.acceptance:
                if i in x[0]:
                    self.AFD.remove(x)
                    self.AFD.append(x)
        for x in self.AFD:
            flag = False
            containsAcceptance = False
            for i in x[1]:
                if i != None and x[1].index(i) != index:
                    flag = True
            if flag == False and x[0] == self.start:
                self.start = x[1][index]

            for i in self.acceptance:
                if i in x[0]:
                    containsAcceptance = True

            if flag == False and x[1][index] != None and containsAcceptance is False:
                for i in range(len(self.AFD)):
                    for ii in range(len(self.AFD[i][1])):
                        if type(self.AFD[i][1][ii]) == list and sorted(self.AFD[i][1][ii]) == sorted(x[0]):
                            self.AFD[i][1][ii] = sorted(x[1][index])
                        elif type(self.AFD[i][1][ii]) != list and sorted([self.AFD[i][1][ii]]) == sorted(x[0]):
                            self.AFD[i][1][ii] = sorted(x[1][index])
                        else:
                            pass
                remove.append(x)
            if flag == False and x[1][index] != None and containsAcceptance is True:
                for i in range(len(self.AFD)):

                    if self.AFD[i][0] == x[1][index]:
                        for ii in range(len(self.symbols)):
                            self.AFD[self.AFD.index(x)][1][ii] = self.AFD[i][1][ii]


        for x in remove:
            self.AFD.remove(x)

    """
    Esta es la funcion madre para el sistema de AFN a AFD, aqui se crea la tabla de transiciones, depende completamente de los indices de las listas
    de los valores de simbolos y estados.

    Tambien se llaman otras funciones como la de defineAFD o modifyStructure, entre otras.
    """
    def toAFD(self):
        self.transitionTable = [[None for _ in range(len(self.symbols))] for _ in range(len(self.states))]


        for _ in range(len(self.transitions)):

            startStatus = self.transitions[_][0]
            transition = self.transitions[_][1]
            endStatus = self.transitions[_][2]

            if transition == "&":
                endStatus = self.find3scope(endStatus, transitions=[])
                #endStatus.append(startStatus)

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
        #print(self.states)
        self.defineAFD()
        self.cleanAFD()


        newAcceptance = []

        #print(self.AFD)

        for x in self.AFD:
            for i in self.acceptance:
                if i in x[0] or i == self.acceptance:
                    newAcceptance.append(x[0])

        #print(self.acceptance, self.AFD)

        self.acceptance = newAcceptance

        self.modifyStateStructure()

        newStates = []
        newTransitions = []
        for x in self.AFD:
            newStates.append(x[0])
            for i in self.symbols:
                if i != '&' and i != None:
                    newTransitions.append((x[0], i, x[1][self.symbols.index(i)]))
                else:
                    for ii in self.symbols:
                        if ii != '&' and ii != None and (x[0], ii, x[1][self.symbols.index(ii)]) not in newTransitions:
                            newTransitions.append((x[0], ii, x[1][self.symbols.index(ii)]))

        self.states = newStates
        self.transitions = newTransitions


        self.writeTxt('respuestas/Conversion_AFN_AFD.txt', self.states, self.symbols, self.start, self.acceptance,
                      self.transitions, 'conversion')


    """
    Ahora, para trabajar de forma mas ordenada se deben cambiar todos los esados a un mismo formato, en este caso decidimos SX
    se debe determinar si contiene epsilon o no, pues la forma de trabajar es distinta dependiendo del escenario y luego se
    """
    def modifyStateStructure(self):
        prefix = 'S'
        index = 0
        for x in range(len(self.AFD)):
            state = self.AFD[x][0]
            if state in self.acceptance:
                self.acceptance[self.acceptance.index(state)] = prefix + str(index)

            if state == self.start:
                self.start = prefix + str(index)

            for i in range(len(self.AFD)):
                for ii in range(len(self.AFD[i][1])):
                    if self.AFD[i][1][ii] is not None and self.AFD[x][0] is not None and sorted(self.AFD[i][1][ii]) == sorted(self.AFD[x][0]):
                        self.AFD[i][1][ii] = prefix + str(index)

                    if type(self.AFD[i][1][ii]) != list and len(self.AFD[x][0]) == 1 and self.AFD[i][1][ii] == \
                            self.AFD[x][0][0]:
                        self.AFD[i][1][ii] = prefix + str(index)

            self.AFD[x][0] = prefix + str(index)

            index += 1

    """
    Funcion que se encarga de realizar o partir los grupos dependiendo a cual correspondan.
    """
    def setMaker(self, dict):

        statesSets, u_vals = [], []
        for i in range(len(list(dict.items()))):
            sT = list(dict.items())[i]  # sT => Tuple of state and its transitions
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


    """
    Esta funcion tiene el objetivo de realizar de establecer a que grupo corresponde cada estado y con ello poder hacer la
    particion de grupos posteriormente.
    """
    def grouping(self, subGroups, nonAccepting, symbols, transitions):

        newGroups = []
        dict = {key: [] for key in nonAccepting}

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


    """
    Esta funcion se encarga de hacer la particion de grupos hasta que se cumpla condicion en la cual la particion de grupos
    no tenga ning??n cambio y para el while loop. Obteniendo de esta forma la particion de grupos.
    """
    def partition(self):
        # Start with initial partition accepting and non-accepting states
        accepting = self.acceptance
        nonAccepting = [i for i in self.states if i not in accepting]

        # Making subsets
        subSets = [accepting, nonAccepting]

        bandera = True
        while bandera:
            prevGroups = subSets
            prevSyms = nonAccepting
            subSets = self.grouping(subSets, prevSyms, self.symbols, self.transitions)

            if sorted(prevGroups) == sorted(subSets):
                bandera = False

        newSD = {key: [] for key in range(len(subSets))}

        for indx in range(len(subSets)):
            newSD[indx] += subSets[indx]

        for indx in range(len(newSD.keys())):
            lastSVal = self.states[-1][-1]
            newVal = int(lastSVal) + indx + 1
            newState = 'S' + str(newVal)
            newSD[newState] = newSD.pop(indx)
        return newSD


    """
    Funcion para escribir archivos de texto con las respuestas.
    """
    def writeTxt(self, fileName, states, symbols, start, accepting, transitions, type, dict={}):
        f = open(fileName, "w+")
        f.write("ESTADOS = " + str(states) + '\n')
        f.write("SIMBOLOS = " + str(symbols) + '\n')
        f.write("INICIO = " + str(start) + '\n')
        f.write("ACEPTACION = " + str(accepting) + '\n')
        f.write("TRANSICIONES = [")
        for indx in range(len(transitions)):
            if indx < 1:
                f.write(str(transitions[indx]) + ',\n')
            if indx == len(transitions) - 1:
                f.write('\t\t\t\t' + str(transitions[indx]) + ']')
            elif indx >= 1:
                f.write('\t\t\t\t' + str(transitions[indx]) + ',\n')

        f.write('\n')

        if type == 'mini':
            f.write("NUEVA REPRESENTACION DE ESTADOS = {")
            for index, (k, v) in enumerate(dict.items()):
                if index < 1:
                    f.write("'" + str(k) + "': " + str(v) + ',\n')
                if index == len(dict) - 1:
                    f.write('\t\t\t\t\t\t\t\t' + "   '" + str(k) + "': " + str(v) + '}')
                elif index >= 1:
                    f.write('\t\t\t\t\t\t\t\t' + "   '" + str(k) + "': " + str(v) + ',\n')
        f.close()

    def minimizeAFD(self, statesD):
        # Replacing states in list by new states
        newStates = []  # Creating new states list
        for k, v in statesD.items():
            newStates.append(k)

        # Replacing by new start state
        newStart = []  # Creating new start list
        for k, v in statesD.items():
            if self.start in v:
                newStart.append(k)

        #Verifying states 
        newSyms = []
        for sym in self.symbols:
            if (sym == '&'): continue 
            newSyms.append(sym)

        # Creating new aceptance list
        newAcceptance = []
        for element in self.acceptance:
            newAcceptance.append(element)

        # Replacing new acceptance states
        for k, v in statesD.items():
            for indx in range(len(newAcceptance)):
                if newAcceptance[indx] in v:
                    newAcceptance[indx] = k
        newAcceptance = list(dict.fromkeys(newAcceptance))  # In case elements are duplicated

        # Creating new transition list
        newTransitions = []
        for element in self.transitions:
            if(element[2] == None): continue
            newTransitions.append(element)

        # Converting lists to tuples
        cList = [list(i) for i in newTransitions]

        # Replacing new states in transitions list
        for transition in cList:
            for k, v in statesD.items():
                if transition[0] in v:
                    if transition[2] == None: continue
                    transition[0] = k
                if transition[2] in v:
                    if transition[2] == None: continue
                    transition[2] = k

        # Removing duplicates
        noDuplicatesList = sorted(set(tuple(l) for l in cList))
        newTransitions = noDuplicatesList

        self.writeTxt('respuestas/Minimizacion_AFD.txt', newStates, newSyms, newStart, newAcceptance,
                      newTransitions, 'mini', statesD)

    def basic_automata(current_status, operand):
        return Automata(
            states=[f'{current_status}', f'{current_status + 1}'],
            acceptance=[f'{current_status + 1}'],
            symbols=[operand],
            start=[f'{current_status}'],
            transitions=[(f'{current_status}', operand, f'{current_status + 1}')]
        )

    def fromRegex(regex):
        posfixExpression = regex.toPosfix()
        print(f"La expresi??n postfix es: {posfixExpression}")
        regex_splitted = [char for char in posfixExpression]
        stack = []
        current_status = 0
        for item in regex_splitted:
            # Algorithm
            # 1. If it is an item, append to the stack
            # 2. If it is an operation, do the calculation and append result to the stack.
            # 3. Finish when there is only one element left on the stack and is an automata.
            if item not in ["*", "@", "|"]:
                # It is a character
                stack.insert(0, item)
            elif item in ["*", "@", "|"]:
                if item == "@":
                    # Concat
                    rightOperand = stack.pop(0)
                    leftOperand = stack.pop(0)
                    if not isinstance(leftOperand, Automata):
                        leftOperand = Automata.basic_automata(current_status, leftOperand)
                        current_status += 2
                    if not isinstance(rightOperand, Automata):
                        rightOperand = Automata.basic_automata(current_status, rightOperand)
                        current_status += 1
                    # Create the result Automata
                    result_automata = Automata(
                        states=list(dict.fromkeys(leftOperand.states + rightOperand.states)),
                        acceptance=rightOperand.acceptance,
                        start=leftOperand.start,
                        symbols=list(dict.fromkeys(leftOperand.symbols + rightOperand.symbols + ["&"])),
                        transitions=leftOperand.transitions + rightOperand.transitions + [
                            (leftOperand.acceptance[0], "&", rightOperand.start[0])]
                    )
                    stack.insert(0, result_automata)
                    current_status += 1
                elif item == "|":
                    # Union
                    rightOperand = stack.pop(0)
                    leftOperand = stack.pop(0)
                    if not isinstance(leftOperand, Automata):
                        leftOperand = Automata.basic_automata(current_status, leftOperand)
                        current_status += 2
                    if not isinstance(rightOperand, Automata):
                        rightOperand = Automata.basic_automata(current_status, rightOperand)
                        current_status += 1
                    # Create the result automata
                    current_status += 1
                    start_state = current_status
                    current_status += 1
                    end_state = current_status
                    result_automata = Automata(
                        states=list(dict.fromkeys(leftOperand.states + rightOperand.states)) + [f'{start_state}',
                                                                                                f'{end_state}'],
                        acceptance=[f'{end_state}'],
                        start=[f'{start_state}'],
                        symbols=list(dict.fromkeys(leftOperand.symbols + rightOperand.symbols + ["&"])),
                        transitions=leftOperand.transitions + rightOperand.transitions + [
                            (f'{start_state}', "&", leftOperand.start[0]),
                            (f'{start_state}', "&", rightOperand.start[0]),
                            (leftOperand.acceptance[0], "&", f'{end_state}'),
                            (rightOperand.acceptance[0], "&", f'{end_state}'),
                        ]
                    )
                    stack.insert(0, result_automata)
                    current_status += 1

                elif item == "*":
                    # Kleene
                    operand = stack.pop(0)
                    if not isinstance(operand, Automata):
                        operand = Automata.basic_automata(current_status, operand)
                        current_status += 1
                    # Create the result automata
                    current_status += 1
                    start_state = current_status
                    current_status += 1
                    end_state = current_status
                    result_automata = Automata(
                        states=list(dict.fromkeys(operand.states)) + [f'{start_state}',
                                                                      f'{end_state}'],
                        acceptance=[f'{end_state}'],
                        start=[f'{start_state}'],
                        symbols=list(dict.fromkeys(operand.symbols + ["&"])),
                        transitions=operand.transitions + [
                            (operand.acceptance[0], "&", operand.start[0]),
                            (f'{start_state}', "&", f'{end_state}'),
                            (f'{start_state}', "&", operand.start[0]),
                            (operand.acceptance[0], "&", f'{end_state}'),
                        ]
                    )
                    stack.insert(0, result_automata)
                    current_status += 1

        stack[0].writeTxt('respuestas/FromRegex_To_AFN.txt', stack[0].states, stack[0].symbols, stack[0].start, stack[0].acceptance,
                      stack[0].transitions, 'FromRegex_To_AFN')

        return stack[0]

    def e_closure(self, state):
        closure = [state]
        # Get index for starting state
        idx = self.states.index(state)
        # Start building the closure
        for i in range(0,len(self.matrix[idx])):
            if self.matrix[idx][i].count("&") > 0 and i != idx:
                closure = closure + self.e_closure(self.states[i])

        return closure

    def e_closures(self, states):
        for state in states:
            c = self.e_closure(state)
            states = states + c
        return list(dict.fromkeys(states))

    def move(self, s, c):
        end_states = []
        for state in s:
            # Get the index on the state
            idx = self.states.index(state)
            for i in range(0, len(self.matrix[idx])):
                if self.matrix[idx][i].count(c) > 0:
                    end_states.append(self.states[i])
        return end_states


    def simulate_afd(self, word):
        acceptance = False
        state = self.start
        for char in word:
            # Find a possible transition
            if char not in self.symbols:
                return False
            flag = False
            for t in self.transitions:
                if t[0] == state and t[1] == char and t[2] is not None:
                    # found a transition - go to the next state
                    print(t)
                    state = t[2]
                    flag = True
                    break

            if flag == False:
                return False
        if self.acceptance.count(state) > 0:
            acceptance = True

        return acceptance



    def simulate_afn(self, word):
        s = self.e_closure(self.start[0])
        for char in word:
            s = self.e_closures(self.move(s, char))
        for state in s:
            if self.acceptance.count(state) > 0: return True
        return False

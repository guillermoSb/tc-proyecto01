from distutils.ccompiler import new_compiler
from textwrap import indent
from typing import final
from regex import Regex
from automata import Automata

x = Automata(states=["0", "1", "2", "3", "4", "5", "6", "7"], symbols=["a", "b", "&"], start=["0"], acceptance=["7"],
             transitions=[("0", "&", "1"), ("0", "&", "4"), ("1", "a", "2"), ("1", "&", "3"), ("2", "a", "3"),
                          ("3", "&", "7"), ("7", "&", "0"), ("4", "b", "5"), ("4", "&", "6"), ("5", "b", "6"),
                          ("6", "&", "7")])
y = Automata(states=["A", "B", "C", "D", "E"], symbols=["a", "b"], start=["A"], acceptance=["E"],
             transitions=[("A", "a", "B"), ("A", "b", "C"), ("B", "a", "B"), ("B", "b", "D"), ("C", "a", "B"),
                          ("C", "b", "C"), ("D", "a", "B"), ("D", "b", "E"), ("E", "a", "B"), ("E", "b", "C")])
z = Automata(states=["A", "B", "C", "D", "E", "F", "G", "H"], symbols=["0", "1"], start=["A"], acceptance=["C"],
             transitions=[("A", "0", "B"), ("A", "1", "F"), ("B", "0", "G"), ("B", "1", "C"), ("C", "0", "A"),
                          ("C", "1", "C"), ("D", "0", "C"), ("D", "1", "G"), ("E", "0", "H"), ("E", "1", "F"),
                          ("F", "0", "C"), ("F", "1", "G"), ("G", "0", "G"), ("G", "1", "E"), ("H", "0", "G"),
                          ("H", "1", "C")])
k = Automata(states=["A", "B", "C", "D", "E", "F", "G", "H"], symbols=["a", "b"], start=["A"], acceptance=["C", "H"],
             transitions=[("A", "a", "B"), ("A", "b", "E"), ("B", "a", "F"), ("B", "b", "C"), ("C", "a", "D"),
                          ("C", "b", "G"), ("D", "a", "D"), ("D", "b", "D"), ("E", "a", "B"), ("E", "b", "E"),
                          ("F", "a", "B"), ("F", "b", "E"), ("G", "a", "D"), ("G", "b", "H"), ("H", "a", "D"),
                          ("H", "b", "G")])
#
# expectedAutomata = Automata(
#         states=['9', '10', '0', '1', '2', '3', '4', '5', '7', '8'],
#         symbols=["a", "b", "&"],
#         start=["9"],
#         acceptance=["8"],
#         transitions=[('9', 'a', '10'), ('0', 'a', '1'), ('2', 'b', '3'), ('4', '&', '0'), ('4', '&', '2'),
#                      ('1', '&', '5'), ('3', '&', '5'), ('5', '&', '4'), ('7', '&', '8'), ('7', '&', '4'),
#                      ('5', '&', '8'), ('10', '&', '7')]
#     )


# Act

# z.toAFD()
# z.minimizeAFD(z.partition())

#automataFromRegex.toAFD()

# result = automataFromRegex.simulate_afd("abaaabbb")

#result = automataFromRegex.simulate_afd("babbbaaaaab")
# Assert
# print(result)
# x.partition()


# Si existe un automata
# 2. Convertir a AFD
    # automataFromRegex.toAFD()
    # exportar archivo
# 3. Minimizar AFD
    # Llamar metodo de minimizar y exportar archivo
# 4. Simular AFN
# Pedir cadena a simular: aaasdf
# Imprimir true o false si la cadena si es aceptada
#automataFromRegex.simulate_afn(aaasdf)
# 5. Simular AFD
# Pedir cadena a simular: aaasdf
# automataFromRegex.simulate_afd(aaasdf)
# Imprimir true o false si la cadena si es aceptada


def menu():
    print('\nOpciones:\n1. Ingresar regex\
           \n2. Convertir a AFD \n3. Minimizar AFD \n4. Simular AFN \n5. Simular AFD \n6. Salir \n')

def options():
    print('\nProyecto 1 - Teoría de la computación')
    menu()
    option = int(input('Elija una opción: '))
    while option != 6:
        if option == 1: 
            regex = str(input('Ingrese cadena regex: '))
            regex = Regex(regex)
            automataFromRegex = Automata.fromRegex(regex)
        
        elif option == 2: 

            print('\nConversión de automata a AFD')
            regex = str(input('Ingrese cadena regex: '))
            regex = Regex(regex)
            automataFromRegex = Automata.fromRegex(regex)
            automataFromRegex.toAFD()

        elif option == 3: 
            print('\nMinimización a AFD')
            regex = str(input('Ingrese cadena regex: '))
            regex = Regex(regex)
            automataFromRegex = Automata.fromRegex(regex)
            automataFromRegex.toAFD()
            automataFromRegex.minimizeAFD(automataFromRegex.partition())

        elif option == 4: 
            print('\nSimulación AFN')
            regex = str(input('Ingrese cadena regex para generar automata: '))
            regex = Regex(regex)
            regex2 = str(input('Ingrese cadena regex para comprobar si es aceptada: '))
            automataFromRegex = Automata.fromRegex(regex)
            if automataFromRegex.simulate_afn(regex2):
                print('\nLa cadena es aceptada')
            else:
                print('\nLa cadena no es aceptada')

        elif option == 5: 
            print('\nSimulación AFD')
            regex = str(input('Ingrese cadena regex para generar automata: '))
            regex = Regex(regex)
            regex2 = str(input('Ingrese cadena regex para comprobar si es aceptada: '))
            automataFromRegex = Automata.fromRegex(regex)
            automataFromRegex.toAFD()
            if (automataFromRegex.simulate_afd(regex2)):
                print('\nLa cadena es aceptada')
            else:
                print('\nLa cadena no es aceptada')

        else: print('\nOpcion invalida\n')

        menu()
        option = int(input('Elija una opción: '))


options()

# options()

# regex = Regex(regex)


# k.minimizeAFD(k.partition())


regex = Regex('a@(a|b)*@b@a@b@(a|b)*@(a|b)*@(a|b)*')
automataFromRegex = Automata.fromRegex(regex)
automataFromRegex.toAFD()
print(automataFromRegex.simulate_afd('aaaaaaaabababababababbbbbb'))

# automataFromRegex.minimizeAFD(automataFromRegex.partition())


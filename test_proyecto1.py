from regex import Regex
from proyecto1 import Automata

def test_converts_regex_to_posfix():
    # Arrange
    regex = Regex("a@(a|b)*@b")
    # Act
    posfixExpression = regex.toPosfix()
    # Assert
    assert posfixExpression == "aab|*@b@"

def test_converts_regex_to_posfix2():
    # Arrange
    regex = Regex("a@b")
    # Act
    posfixExpression = regex.toPosfix()
    # Assert
    assert posfixExpression == "ab@"


def test_can_convert_case_1_thompson():
    # Concat
    # Arrange
    regex = Regex("a@b")
    # Act
    automataFromRegex = Automata.fromRegex(regex)
    # Assert
    expectedAutomata = Automata(
        states=["0", "1", "2", "3"],
        symbols=["a", "b", "&"],
        start=["0"],
        acceptance=["3"],
        transitions=[("0", "a", "1"),
                     ("1", "&", "2"),
                     ("2", "b", "3")]
        )
    assert automataFromRegex.states == expectedAutomata.states
    assert automataFromRegex.acceptance == expectedAutomata.acceptance
    assert automataFromRegex.start == expectedAutomata.start
    assert len(automataFromRegex.transitions) == len(expectedAutomata.transitions)
    for t in expectedAutomata.transitions:
        idx = automataFromRegex.transitions.index(t)
        assert idx >= 0



def test_can_convert_case_2_thompson():
    # Union
    # Arrange
    regex = Regex("a|b")
    # Act
    automataFromRegex = Automata.fromRegex(regex)
    # Assert
    expectedAutomata = Automata(
        states=["0", "1", "2", "3", "4", "5"],
        symbols=["a", "b", "&"],
        start=["4"],
        acceptance=["5"],
        transitions=[
                ("4", "&", "0"),
                ("4", "&", "2"),
                ("0", "a", "1"),
                ("1", "&", "5"),
                ("2", "b", "3"),
                ("3", "&", "5"),

            ]
        )
    assert automataFromRegex.states == expectedAutomata.states
    assert automataFromRegex.acceptance == expectedAutomata.acceptance
    assert automataFromRegex.start == expectedAutomata.start
    assert len(automataFromRegex.transitions) == len(expectedAutomata.transitions)
    for t in expectedAutomata.transitions:
        idx = automataFromRegex.transitions.index(t)
        assert idx >= 0



def test_can_convert_case_3_thompson():
    # Union
    # Arrange
    regex = Regex("a*")
    # Act
    automataFromRegex = Automata.fromRegex(regex)
    # Assert
    expectedAutomata = Automata(
        states=["0", "1", "2", "3"],
        symbols=["a", "b", "&"],
        start=["2"],
        acceptance=["3"],
        transitions=[
                ("2", "&", "0"),
                ("0", "a", "1"),
                ("1", "&", "3"),
                ("2", "&", "3"),
                ("1", "&", "0"),
            ]
        )
    assert automataFromRegex.states == expectedAutomata.states
    assert automataFromRegex.acceptance == expectedAutomata.acceptance
    assert automataFromRegex.start == expectedAutomata.start
    assert len(automataFromRegex.transitions) == len(expectedAutomata.transitions)
    for t in expectedAutomata.transitions:
        idx = automataFromRegex.transitions.index(t)
        assert idx >= 0


def test_can_convert_complex_automata_1():
    # Union
    # Arrange
    regex = Regex("a@(a|b)")
    # Act
    automataFromRegex = Automata.fromRegex(regex)
    # Assert
    expectedAutomata = Automata(
        states=["0", "1", "2", "3", "4", "5", "6", "7"],
        symbols=["a", "b", "&"],
        start=["6"],
        acceptance=["5"],
        transitions=[
            ("6", "a", "7"),
            ("7", "&", "4"),
            ("4", "&", "2"),
            ("4", "&", "0"),
            ("2", "b", "3"),
            ("0", "a", "1"),
            ("3", "&", "5"),
            ("1", "&", "5"),
        ]
    )
    assert len(automataFromRegex.states) == len(expectedAutomata.states)
    for s in expectedAutomata.start:
        idx = automataFromRegex.states.index(s)
        assert idx >= 0
    assert automataFromRegex.acceptance == expectedAutomata.acceptance
    assert automataFromRegex.start == expectedAutomata.start
    assert len(automataFromRegex.transitions) == len(expectedAutomata.transitions)
    for t in expectedAutomata.transitions:
        idx = automataFromRegex.transitions.index(t)
        assert idx >= 0

def test_can_convert_complex_automata_2():
    # Arrange
    regex = Regex("a@(a|b)*")
    # Act
    automataFromRegex = Automata.fromRegex(regex)
    # Assert
    expectedAutomata = Automata(
        states=['9', '10', '0', '1', '2', '3', '4', '5', '7', '8'],
        symbols=["a", "b", "&"],
        start=["9"],
        acceptance=["8"],
        transitions=[('9', 'a', '10'), ('0', 'a', '1'), ('2', 'b', '3'), ('4', '&', '0'), ('4', '&', '2'),
                     ('1', '&', '5'), ('3', '&', '5'), ('5', '&', '4'), ('7', '&', '8'), ('7', '&', '4'),
                     ('5', '&', '8'), ('10', '&', '7')]
    )
    assert len(automataFromRegex.states) == len(expectedAutomata.states)
    for s in expectedAutomata.start:
        idx = automataFromRegex.states.index(s)
        assert idx >= 0
    assert automataFromRegex.acceptance == expectedAutomata.acceptance
    assert automataFromRegex.start == expectedAutomata.start
    assert len(automataFromRegex.transitions) == len(expectedAutomata.transitions)
    for t in expectedAutomata.transitions:
        idx = automataFromRegex.transitions.index(t)
        assert idx >= 0

def test_can_get_e_closure():
    # Arrange
    regex = Regex("a@b")
    automataFromRegex = Automata.fromRegex(regex)
    # Act
    closure = automataFromRegex.e_closure("1")
    # Assert
    closure_items = ["1","2"]
    assert len(closure) == 2
    assert closure == closure_items

def test_can_get_e_closure_2():
    # Arrange
    regex = Regex("a*")
    automataFromRegex = Automata.fromRegex(regex)
    # Act
    closure = automataFromRegex.e_closure("1")
    # Assert
    print(closure)
    closure_items = ["1", "0", "3"]
    assert len(closure) == len(closure_items)
    assert closure == closure_items

def test_can_simulate_afn():
    # Arrange
    regex = Regex("a@b")
    automataFromRegex = Automata.fromRegex(regex)
    # Act
    result = automataFromRegex.simulate_afn("ab")
    # Assert
    assert result


def test_can_simulate_afn_2():
    # Arrange
    regex = Regex("a*")
    automataFromRegex = Automata.fromRegex(regex)
    # Act
    result = automataFromRegex.simulate_afn("aaaaaaab")
    # Assert
    assert result

def test_can_simulate_afn_3():
    # Arrange
    regex = Regex("a@(a|b)*")
    automataFromRegex = Automata.fromRegex(regex)
    # Act
    result = automataFromRegex.simulate_afn("aaaabbb")
    # Assert
    assert result

def test_can_simulate_afn_4():
    # Arrange
    regex = Regex("(b|b)*@a@b@b@(a|b)*")
    automataFromRegex = Automata.fromRegex(regex)
    # Act
    result = automataFromRegex.simulate_afd("babbaaaaa")
    # Assert
    assert result

def test_can_create_syntax_tree():
    # Arrange
    regex = Regex("a@(a|b)*@b@#")
    # Act
    tree = regex.sintax_tree()
    # Assert
    assert tree.right_child.value == "#"
    assert tree.left_child.value == '@'
    assert tree.left_child.right_child.value == 'b'
    assert tree.left_child.left_child.value == "@"
    assert tree.left_child.left_child.right_child.value == "*"
    assert tree.left_child.left_child.right_child.single_child
    assert tree.left_child.left_child.right_child.middle_child.value == "|"
    assert tree.left_child.left_child.right_child.middle_child.left_child.value == "a"
    assert tree.left_child.left_child.right_child.middle_child.right_child.value == "b"
    assert tree.left_child.left_child.left_child.value == "a"
    assert tree.left_child.left_child.left_child.right_child is None
    assert tree.left_child.left_child.left_child.left_child is None

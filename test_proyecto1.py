from regex import Regex

def test_converts_regex_to_posfix():
    # Arrange
    regex = Regex("a@(a+b)*@b")
    # Act
    posfixExpression = regex.toPosfix()
    # Assert
    assert posfixExpression == "aab+*@b@"


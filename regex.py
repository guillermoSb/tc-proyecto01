


class Regex:
    def __init__(self, expression):
        self.expression = expression

    def toPosfix(self):
        input = [char for char in self.expression]
        operator_stack = []  # Stack for operators
        output_queue = ""    # Output expression
        # Precedences for the operations
        precedences = {
            "*": 2,
            "@": 1,
            "+": 0,
            "(": -1,
            ")": -1
        }
        # Start Shunting-Yard Algorithm
        for char in input:
            if char not in ["*", "@", "+", "(", ")"]:
                output_queue += char
            elif char in ["*", "@", "+"]:
                while len(operator_stack) > 0:
                    if precedences[operator_stack[0]] < precedences[char]:
                        break
                    output_queue += operator_stack.pop(0)
                operator_stack.insert(0, char)  # Insert the operator at the start of the stack
            elif char == "(":
                operator_stack.insert(0, char)
            elif char == ")":
                while len(operator_stack) > 0:
                    popped_item = operator_stack.pop(0)
                    if popped_item == "(":
                       break
                    output_queue += popped_item
        # Pop all the remaining elements
        while len(operator_stack) > 0:
            output_queue += operator_stack.pop(0)
        return output_queue

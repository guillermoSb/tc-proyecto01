from node import Node


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
            "|": 0,
            "(": -1,
            ")": -1
        }
        # Start Shunting-Yard Algorithm
        for char in input:
            if char not in ["|", "@", "+", "(", ")"]:
                output_queue += char
            elif char in ["|", "@", "+"]:
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

    def sintax_tree(self):
        posfix = self.toPosfix()
        tree_stack = [] # Stack to keep the operations
        for item in posfix:
            if item not in ["*", "@", "|"]:
                # It is a character, append to the tree_stack
                tree_stack.insert(0, item)
            elif item in ["*", "@", "|"]:
                if item in ["@", "|"]:
                    rightOperand = tree_stack.pop(0)
                    leftOperand = tree_stack.pop(0)
                    # Create the nodes if the item is a character
                    if not isinstance(leftOperand, Node):
                        leftOperand = Node(value=leftOperand, right_child=None, left_child=None)
                    if not isinstance(rightOperand, Node):
                        rightOperand = Node(value=rightOperand, right_child=None, left_child=None)

                    new_node = Node(left_child=leftOperand, right_child=rightOperand, value=item)
                else:
                    # It is a * only has one middle child
                    operand = tree_stack.pop(0)
                    # Create the nodes if the item is a character
                    if not isinstance(operand, Node):
                        operand = Node(operand, value=rightOperand)
                    new_node = Node(middle_child=operand,value=item, left_child=None, right_child=None)
                # Add the new node to the tree stack
                tree_stack.insert(0, new_node)
        return tree_stack[0]


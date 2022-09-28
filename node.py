class Node:
    def __init__(self, left_child, right_child,value, middle_child = None):
        # In the case that the node only has a middle child assign a boolean to make the calculations easier
        if middle_child is not None:
            self.single_child = True
            self.middle_child = middle_child
        else:
            self.left_child = left_child
            self.right_child = right_child
        self.value = value

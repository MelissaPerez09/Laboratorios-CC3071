"""
DirectAFD.py
Convert the regular expression to an DFA using the direct method
"""

from Parser import *
from ShuntingYard import *

class DirectAFD:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Step 1: Increase r
def increaseR(regex):
    return regex + '#.'

# Step 2: Construct a syntax tree t from r
def construct_syntax_tree(postfix):
    stack = []

    for token in postfix:
        if token.isalnum():
            node = DirectAFD(token)
            stack.append(node)
        elif token in ['.', '|', '#']:  # Include '#' as an operator
            if token == '#':
                # Create a leaf node representing '#' and append to the stack
                node = DirectAFD(token)
                stack.append(node)
            else:
                right = stack.pop()
                left = stack.pop()
                node = DirectAFD(token)
                node.left = left
                node.right = right
                stack.append(node)
        elif token == '*':
            if stack:
                operand = stack.pop()
                node = DirectAFD(token)
                node.left = operand
                stack.append(node)
            else:
                print("Error: Not enough operands in stack")
                return None

    if len(stack) != 1:
        print("Error: Invalid postfix expression")
        return None

    return stack.pop()

# Step 3: Label the leaves of the syntax tree
def label_leaves(node, label):
    if node is not None:
        if node.left is None and node.right is None:
            node.value = label
            return label + 1
        label = label_leaves(node.left, label)
        label = label_leaves(node.right, label)
    return label

# Step 4: Calculate the nullable function
def calculate_nullable(node):
    if node is None:
        return False
    
    if node.value == '#':
        return True
    elif node.value == '.':
        return calculate_nullable(node.left) and calculate_nullable(node.right)
    elif node.value == '|':
        return calculate_nullable(node.left) or calculate_nullable(node.right)
    elif node.value == '*':
        return True
    
    return False

# Step 5: Calculate the first position function
def calculate_first_position(node, first_pos, value_map):
    if node is None:
        return

    if node.value in value_map:
        char = value_map[node.value]
        first_pos[char].add(node)
    elif node.value == '.':
        if calculate_nullable(node.left):
            calculate_first_position(node.left, first_pos, value_map)
            calculate_first_position(node.right, first_pos, value_map)
        else:
            calculate_first_position(node.left, first_pos, value_map)
    elif node.value == '|':
        calculate_first_position(node.left, first_pos, value_map)
        calculate_first_position(node.right, first_pos, value_map)
    elif node.value == '*':
        calculate_first_position(node.left, first_pos, value_map)

# Step 6: Calculate the last position function
def calculate_last_position(node, last_pos, value_map):
    if node is None:
        return

    if node.value in value_map:
        char = value_map[node.value]
        last_pos[char].add(node)
    elif node.value == '.':
        if calculate_nullable(node.right):
            calculate_last_position(node.left, last_pos, value_map)
            calculate_last_position(node.right, last_pos, value_map)
        else:
            calculate_last_position(node.right, last_pos, value_map)
    elif node.value == '|':
        calculate_last_position(node.left, last_pos, value_map)
        calculate_last_position(node.right, last_pos, value_map)
    elif node.value == '*':
        calculate_last_position(node.left, last_pos, value_map)

# Step 7: Calculate the follow position function
def calculate_follow_position(node, follow_pos, first_pos, last_pos):
    if node is None:
        return

    if node.value == '.':
        if node.left and node.right:
            for position in last_pos[node.left.position]:
                follow_pos[position].update(first_pos[node.right.position])
    elif node.value == '*':
        if node.left:
            for position in last_pos[node.left.position]:
                follow_pos[position].update(first_pos[node.left.position])

    calculate_follow_position(node.left, follow_pos, first_pos, last_pos)
    calculate_follow_position(node.right, follow_pos, first_pos, last_pos)

def print_syntax_tree(node, indent=0):
    # Helper function to print the syntax tree
    if node is not None:
        print(" " * indent + str(node.value))
        if node.left is not None or node.right is not None:
            print_syntax_tree(node.left, indent + 4)
            print_syntax_tree(node.right, indent + 4)

def collect_unique_values(node, values):
    if node is None:
        return

    collect_unique_values(node.left, values)
    collect_unique_values(node.right, values)

    if isinstance(node.value, int) and node.value not in values:
        values.add(node.value)

def main():
    #regex = "(a*|b*)c"
    regex = "(a|b)*abb"
    parsed_regex = parse_regex(regex)
    print(f"\nParsed expression: {parsed_regex}")

    # Shunting Yard
    shunting_yard = ShuntingYard(parsed_regex)
    postfix_expression = shunting_yard.shuntingYard()
    print(f"\nPostfix expression: {postfix_expression}")
    
    increased = increaseR(postfix_expression)
    syntax_tree = construct_syntax_tree(increased)
    label_leaves(syntax_tree, 1)  # Start labeling from 1
    print_syntax_tree(syntax_tree)
    
    nullable = calculate_nullable(syntax_tree)
    print("Nullable function:", nullable)
    
    unique_values = set()
    collect_unique_values(syntax_tree, unique_values)

    # Map integers to characters
    value_map = {value: chr(value) for value in unique_values}

    first_pos = {char: set() for char in value_map.values()}
    calculate_first_position(syntax_tree, first_pos, value_map)
    print("First position function:")
    for char, positions in first_pos.items():
        print(char, "->", [pos.value for pos in positions])
        
    last_pos = {char: set() for char in value_map.values()}
    calculate_last_position(syntax_tree, last_pos, value_map)
    print("Last position function:")
    for char, positions in last_pos.items():
        print(char, "->", [pos.value for pos in positions])
    
    follow_pos = {position: set() for position in range(len(value_map))}
    calculate_follow_position(syntax_tree, follow_pos, first_pos, last_pos)
    print("Follow position function:")
    for position, follow_positions in follow_pos.items():
        print(position, "->", follow_positions)


if __name__ == "__main__":
    main()

"""
DirectAFD.py
Convert the regular expression to an DFA using the direct method
"""

from Parser import *
from ShuntingYard import *
from graphviz import Digraph

class DirectAFD:
    def __init__(self, value, position=None):
        self.value = value
        self.position = position
        self.left = None
        self.right = None

# Step 1: Increase r
def increaseR(regex):
    return regex + '#.'

# Step 2: Construct a syntax tree t from r
def construct_syntax_tree(postfix):
    stack = []
    position = 0
    for token in postfix:
        if token.isalnum():
            node = DirectAFD(token, position)
            stack.append(node)
            position += 1
        elif token in ['.', '|', '#']:
            if token == '#':
                node = DirectAFD(token, position)
                stack.append(node)
                position += 1
            else:
                right = stack.pop()
                left = stack.pop()
                node = DirectAFD(token)
                node.left = left
                node.right = right
                stack.append(node)
        elif token == '*':
            operand = stack.pop()
            node = DirectAFD(token)
            node.left = operand
            stack.append(node)
    return stack.pop()

# Step 3: Label the leaves of the syntax tree
def label_leaves(node, label=0):
    if node:
        if node.left is None and node.right is None:
            node.position = label
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
    if node.value == '|':
        return calculate_nullable(node.left) or calculate_nullable(node.right)
    if node.value == '.':
        return calculate_nullable(node.left) and calculate_nullable(node.right)
    if node.value == '*':
        return True
    return False

# Step 5: Calculate the first position function
def calculate_first_position(node):
    if node is None:
        return set()
    if node.value in ['a', 'b']:  # Assuming leaf nodes contain 'a' or 'b'
        return {node.position}
    if node.value == '|':
        return calculate_first_position(node.left) | calculate_first_position(node.right)
    if node.value == '.':
        if calculate_nullable(node.left):
            return calculate_first_position(node.left) | calculate_first_position(node.right)
        else:
            return calculate_first_position(node.left)
    if node.value == '*':
        return calculate_first_position(node.left)
    return set()

# Step 6: Calculate the last position function
def calculate_last_position(node):
    if node is None:
        return set()
    if node.value in ['a', 'b']:
        return {node.position}
    if node.value == '|':
        return calculate_last_position(node.left) | calculate_last_position(node.right)
    if node.value == '.':
        if calculate_nullable(node.right):
            return calculate_last_position(node.left) | calculate_last_position(node.right)
        else:
            return calculate_last_position(node.right)
    if node.value == '*':
        return calculate_last_position(node.left)
    return set()

# Step 7: Calculate the follow position function
def calculate_follow_pos(node, follow_pos=None):
    if follow_pos is None:
        follow_pos = {i: set() for i in range(label_leaves(node))}  # Initialize follow_pos with positions

    if node.value == '.':
        # Concatenation: For each position p in last_pos(left), add all positions in first_pos(right) to follow_pos[p]
        for pos in calculate_last_position(node.left):
            follow_pos[pos].update(calculate_first_position(node.right))

    elif node.value == '*':
        # Kleene star: For each position p in last_pos(node), add all positions in first_pos(node) to follow_pos[p]
        for pos in calculate_last_position(node):
            follow_pos[pos].update(calculate_first_position(node))

    # Recurse on children
    if node.left:
        calculate_follow_pos(node.left, follow_pos)
    if node.right:
        calculate_follow_pos(node.right, follow_pos)

    return follow_pos

def find_node_by_position(node, position):
    if node is None:
        return None
    if node.position == position:
        return node
    left_result = find_node_by_position(node.left, position)
    if left_result is not None:
        return left_result
    right_result = find_node_by_position(node.right, position)
    if right_result is not None:
        return right_result
    return None

# Step 8: Construct the DFA
def construct_dfa_states_and_transitions(syntax_tree, follow_pos):
    alphabet = {'a', 'b', '0', '1', '2'}  # Ensure this includes all characters in your regex
    start_state = frozenset(calculate_first_position(syntax_tree))
    states = {start_state}
    dfa_transitions = {}
    queue = [start_state]

    while queue:
        current_state = queue.pop(0)
        for char in alphabet:
            next_state = set()
            for pos in current_state:
                node = find_node_by_position(syntax_tree, pos)
                if node and node.value == char:
                    next_state.update(follow_pos.get(pos, set()))

            if next_state:
                next_state_frozen = frozenset(next_state)
                if next_state_frozen not in states:
                    states.add(next_state_frozen)
                    queue.append(next_state_frozen)
                dfa_transitions[(current_state, char)] = next_state_frozen

    return states, dfa_transitions

# Step 9: Construct transition table
def find_accept_states(states, syntax_tree):
    # Assuming the end marker '#' is assigned the highest position
    end_position = max(label_leaves(syntax_tree) - 1, 0)  # Adjust based on your labeling logic
    accept_states = {state for state in states if end_position in state}
    return accept_states

# Step 10: Simulate the DFA
def draw_dfa(dfa_transitions, start_state, accept_states):
    graph = Digraph(format='png', graph_attr={'rankdir': 'LR'})
    
    # Create mapping for states to letters
    states = sorted(set(key[0] for key in dfa_transitions.keys()).union(set(dfa_transitions.values())))
    state_to_number = {state: chr(ord('1') + i) for i, state in enumerate(states)}
    
    graph.attr('node', shape='none', width='0', height='0')
    graph.node('start', label='', shape='none')
    start_state_letter = state_to_number.get(start_state, 'X')  # Default to 'X' if start_state is not found
    graph.edge('start', start_state_letter, arrowhead='vee')
    
    for state, letter in state_to_number.items():
        shape = 'doublecircle' if state in accept_states else 'circle'
        graph.node(letter, label=letter, shape=shape)

    for (from_state, input_char), to_state in dfa_transitions.items():
        from_state_str = state_to_number[from_state]
        to_state_str = state_to_number[to_state]
        graph.edge(from_state_str, to_state_str, label=input_char)
    graph.render('dfa_graph')

def main():
    #regex = "1"
    regex = "(a|b)*abb"
    #regex = "(aa)*(bb)*"
    parsed_regex = parse_regex(regex)  # Ensure this correctly parses the regex
    postfix_expression = ShuntingYard(parsed_regex).shuntingYard()  # Ensure this correctly converts to postfix
    syntax_tree = construct_syntax_tree(postfix_expression)
    label_leaves(syntax_tree)  # Ensure positions are labeled
    
    # Calculate follow_pos
    follow_pos = calculate_follow_pos(syntax_tree)
    
    # Now pass follow_pos as an argument
    states, dfa_transitions = construct_dfa_states_and_transitions(syntax_tree, follow_pos)

    # Print states and transitions for verification
    print("DFA States:")
    for state in states:
        print(f"State: {state}")

    print("\nDFA Transitions:")
    for key, value in dfa_transitions.items():
        print(f"Transition from {key[0]} on '{key[1]}' to {value}")

    start_state = frozenset(calculate_first_position(syntax_tree))
    states, dfa_transitions = construct_dfa_states_and_transitions(syntax_tree, follow_pos)

    # Identify accept states
    accept_states = find_accept_states(states, syntax_tree)

    # Adjusted call to draw_dfa with start_state and accept_states
    draw_dfa(dfa_transitions, start_state, accept_states)

if __name__ == "__main__":
    main()

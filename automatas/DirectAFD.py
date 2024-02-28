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
"""
Increase r
:param regex: The regular expression
Aumenta r en notación postfix con #
"""
def increaseR(regex):
    return regex + '#.'

# Step 2: Construct a syntax tree t from r
"""
Construct a syntax tree t from r
:param postfix: The postfix regular expression
Construye el árbol de sintaxis directamente desde la expresión regular en notación postfix
"""
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
"""
Label the leaves of the syntax tree
:param node: The current node
Etiqueta las hojas del árbol de sintaxis
"""
def label_leaves(node, label=0):
    if node:
        if node.left is None and node.right is None:
            node.position = label
            return label + 1
        label = label_leaves(node.left, label)
        label = label_leaves(node.right, label)
    return label

# Step 4: Calculate the nullable function
"""
Calculate the nullable function
:param node: The current node
Calcula la función anulable
"""
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
"""
Calculate the first position function
:param node: The current node
Calcula la función de primera posición
"""
def calculate_first_position(node):
    if node is None:
        return set()
    if node.value.isalnum() or node.value == '#':
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
"""
Calculate the last position function
:param node: The current node
Calcula la función de última posición
"""
def calculate_last_position(node):
    if node is None:
        return set()
    if node.value.isalnum() or node.value == '#':
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
"""
Calculate the follow position function
:param node: The current node, follow_pos: The follow position dictionary
Calcula la función de posición de seguimiento
"""
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

"""
Find a node by position
:param node: The current node, position: The position to find
Encuentra un nodo por posición
"""
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
"""
Construct the DFA
:param syntax_tree: The syntax tree, follow_pos: The follow position dictionary
Construye el DFA siguiendo el árbol de sintaxis y la función de posición de seguimiento
"""
def construct_dfa_states_and_transitions(syntax_tree, follow_pos):
    alphabet = set()

    def extract_alphabet(node):
        if node:
            if node.value.isalnum():
                alphabet.add(node.value)
            extract_alphabet(node.left)
            extract_alphabet(node.right)
    extract_alphabet(syntax_tree)

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

            next_state_frozen = frozenset(next_state)
            if next_state and next_state_frozen not in states:
                states.add(next_state_frozen)
                queue.append(next_state_frozen)
            if next_state:  # This ensures transitions to empty sets are not created
                dfa_transitions[(current_state, char)] = next_state_frozen

    return states, dfa_transitions

"""
Find accept states
:param states: The states, syntax_tree: The syntax tree
Encuentra los estados de aceptación
"""
# Step 9: Find accept states
def find_accept_states(states, syntax_tree):
    end_position = max(label_leaves(syntax_tree) - 1, 0)
    accept_states = {state for state in states if end_position in state}
    return accept_states

"""
Draw the DFA
:param dfa_transitions: The DFA transitions, start_state: The start state, accept_states: The accept states
Dibuja el DFA
"""
# Step 10: Simulate the DFA
def draw_dfa(dfa_transitions, start_state, accept_states):
    graph = Digraph(format='png', graph_attr={'rankdir': 'LR'})
    
    # Create mapping for states to letters
    states = sorted(set(key[0] for key in dfa_transitions.keys()).union(set(dfa_transitions.values())))
    state_to_number = {state: chr(ord('1') + i) for i, state in enumerate(states)}
    
    graph.attr('node', shape='none', width='0', height='0')
    graph.node('start', label='', shape='none')
    start_state_letter = state_to_number.get(start_state, 'X')
    graph.edge('start', start_state_letter, arrowhead='vee')
    
    for state, letter in state_to_number.items():
        shape = 'doublecircle' if state in accept_states else 'circle'
        graph.node(letter, label=letter, shape=shape)

    for (from_state, input_char), to_state in dfa_transitions.items():
        from_state_str = state_to_number[from_state]
        to_state_str = state_to_number[to_state]
        graph.edge(from_state_str, to_state_str, label=input_char)
    graph.render('dfa_graph')

"""
Apply direct method
:param postfix_expression: The postfix expression
Aplica el método directo para convertir la expresión regular en un DFA con las funciones anteriores
"""
def applyDirect(regex):
    regex = parse_regex(regex)
    postfix = ShuntingYard(regex).shuntingYard()
    aumentada = increaseR(postfix)
    syntax_tree = construct_syntax_tree(aumentada)
    label_leaves(syntax_tree)
    
    follow_pos = calculate_follow_pos(syntax_tree)
    
    states, dfa_transitions = construct_dfa_states_and_transitions(syntax_tree, follow_pos)
    
    start_state = frozenset(calculate_first_position(syntax_tree))
    states, dfa_transitions = construct_dfa_states_and_transitions(syntax_tree, follow_pos)

    accept_states = find_accept_states(states, syntax_tree)
    draw_dfa(dfa_transitions, start_state, accept_states)

    return dfa_transitions, start_state, accept_states

"""
Simulate the direct AFD
:param dfa_transitions: The DFA transitions, start_state: The start state, accept_states: The accept states, input_chain: The input chain
Simula el AFD directamente con una cadena de entrada y devuelve si la cadena es aceptada
"""
def simulate_direct_afd(dfa_transitions, start_state, accept_states, input_chain):
    current_state = start_state
    for symbol in input_chain:
        current_state_tuple = (current_state, symbol)
        if current_state_tuple in dfa_transitions:
            current_state = dfa_transitions[current_state_tuple]
        else:
            return False
    return current_state in accept_states

# programmed by @melissaperez_
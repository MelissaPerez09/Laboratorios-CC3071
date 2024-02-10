"""
Subset.py
Uses subset construction algorithm to convert NFA to DFA
"""

from collections import deque
from graphviz import Digraph

class NFAtoAFDConverter:
    def __init__(self, nfa_states, nfa_symbols, nfa_transitions, nfa_start_state, nfa_accept_states, epsilon="ε"):
        self.nfa_states = nfa_states
        self.nfa_symbols = nfa_symbols
        self.nfa_transitions = nfa_transitions
        self.nfa_start_state = nfa_start_state
        self.nfa_accept_states = nfa_accept_states
        self.epsilon = epsilon
        
        # Initialize AFD structures
        self.afd_states = set()
        self.afd_symbols = set(nfa_symbols) - {epsilon}
        self.afd_transitions = {}
        self.afd_start_state = None
        self.afd_accept_states = set()
        self.convert_nfa_to_afd()

    """
    Epsilon Closure
    :param states: Set of states
    Calcula el cierre epsilon de un conjunto de estados
    """
    def epsilon_closure(self, states):
        epsilon_closure_set = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            if state in self.nfa_transitions and self.epsilon in self.nfa_transitions[state]:
                for next_state in self.nfa_transitions[state][self.epsilon]:
                    if next_state not in epsilon_closure_set:
                        epsilon_closure_set.add(next_state)
                        stack.append(next_state)
        return epsilon_closure_set

    """
    Move
    :param states: Set of states, symbol: Symbol
    Calcula el conjunto de estados a los que se puede llegar desde un conjunto de estados con un símbolo
    """
    def move(self, states, symbol):
        next_states = set()
        for state in states:
            if state in self.nfa_transitions and symbol in self.nfa_transitions[state]:
                next_states.update(self.nfa_transitions[state][symbol])
        return next_states

    """
    Convert NFA to AFD
    Crea los estados y transiciones del AFD a partir del AFN.
    """
    def convert_nfa_to_afd(self):
        start_state_closure = self.epsilon_closure([self.nfa_start_state])
        self.afd_start_state = tuple(start_state_closure)
        self.afd_states.add(self.afd_start_state)
        if any(state in self.nfa_accept_states for state in start_state_closure):
            self.afd_accept_states.add(self.afd_start_state)

        state_queue = deque([start_state_closure])
        while state_queue:
            current_state = state_queue.popleft()
            for symbol in self.afd_symbols:
                next_state_closure = self.epsilon_closure(self.move(current_state, symbol))
                if not next_state_closure:
                    continue
                next_state_closure = tuple(next_state_closure)
                if next_state_closure not in self.afd_states:
                    self.afd_states.add(next_state_closure)
                    state_queue.append(next_state_closure)
                    if any(state in self.nfa_accept_states for state in next_state_closure):
                        self.afd_accept_states.add(next_state_closure)
                self.afd_transitions[(tuple(current_state), symbol)] = next_state_closure

    """
    Visualize the AFD
    Crea un gráfico del AFD
    """
    def visualize_afd(self):
        graph = Digraph(format='png', graph_attr={'rankdir': 'LR'})
        
        # Create mapping for states to letters
        state_to_letter = {state: chr(ord('A') + i) for i, state in enumerate(self.afd_states)}
        
        graph.attr('node', shape='none', width='0', height='0')
        graph.node('start', label='', shape='none')
        graph.edge('start', str(self.afd_start_state), arrowhead='vee')
        
        for state, letter in state_to_letter.items():
            shape = 'doublecircle' if state in self.afd_accept_states else 'circle'
            graph.node(str(state), label=letter, shape=shape)

        for state in self.afd_states:
            shape = 'doublecircle' if state in self.afd_accept_states else 'circle'
            graph.node(str(state), shape=shape)

        for (from_state, symbol), to_state in self.afd_transitions.items():
            graph.edge(str(from_state), str(to_state), label=symbol)

        graph.render('afd_fromAFN')
    
    """
    Simulate the DFA
    :param input_chain: Input chain
    Simula el AFD con una cadena de entrada y devuelve si la cadena es aceptada
    """
    def simulate_dfa(self, input_chain):
        # Start from the DFA's start state
        current_state = self.afd_start_state
        for symbol in input_chain:
            # Transition to the next state based on the current symbol
            current_state_tuple = (current_state, symbol)  # Current state as tuple for lookup
            if current_state_tuple in self.afd_transitions:
                current_state = self.afd_transitions[current_state_tuple]
            else:
                # If there's no transition for this symbol from the current state, the input is not accepted
                return False
        
        # Check if the ending state is one of the accept states
        return current_state in self.afd_accept_states

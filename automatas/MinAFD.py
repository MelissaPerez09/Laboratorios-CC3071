"""
MinAFD.py
Minimization of and AFD using Hopcroft's algorithm
"""

from graphviz import Digraph

class DFAMinimizer:
    def __init__(self, afd_states, afd_symbols, afd_transitions, afd_start_state, afd_accept_states):
        self.afd_states = list(afd_states)
        self.afd_symbols = list(afd_symbols)
        self.afd_transitions = afd_transitions
        self.afd_start_state = afd_start_state
        self.afd_accept_states = set(afd_accept_states)

    """
    Find equivalence classes
    minimización de estados de Hopcroft
    """
    def find_equivalence_classes(self):
        # Initial partition: Accepting and non-accepting states
        P = {frozenset(self.afd_accept_states), frozenset(set(self.afd_states) - self.afd_accept_states)}
        W = P.copy()
        
        while W:
            A = W.pop()
            for c in self.afd_symbols:
                X = set()
                for state in self.afd_states:
                    if (state, c) in self.afd_transitions and self.afd_transitions[(state, c)] in A:
                        X.add(state)
                P_new = set()
                for Y in P:
                    intersection = X.intersection(Y)
                    difference = Y - X
                    if intersection and difference:
                        P_new.add(frozenset(intersection))
                        P_new.add(frozenset(difference))
                        if Y in W:
                            W.remove(Y)
                            W.add(frozenset(intersection))
                            W.add(frozenset(difference))
                        else:
                            if len(intersection) <= len(difference):
                                W.add(frozenset(intersection))
                            else:
                                W.add(frozenset(difference))
                    elif intersection:
                        P_new.add(frozenset(intersection))
                    elif difference:
                        P_new.add(frozenset(difference))
                P = P_new
        return P

    """
    Minimize the AFD
    con las clases de equivalencia encontradas, se minimiza el AFD
    """
    def minimize(self):
        equivalence_classes = self.find_equivalence_classes()

        # Map old states to new states (representative from each equivalence class)
        state_mapping = {}
        for eq_class in equivalence_classes:
            rep = next(iter(eq_class))  # Take one state as representative
            for state in eq_class:
                state_mapping[state] = rep

        # Create new states
        new_states = set(state_mapping.values())

        # Update transitions to point to new states
        new_transitions = {}
        for (state, symbol), to_state in self.afd_transitions.items():
            if (state_mapping[state], symbol) not in new_transitions:
                new_transitions[(state_mapping[state], symbol)] = state_mapping[to_state]

        # Update start and accept states
        new_start_state = state_mapping[self.afd_start_state]
        new_accept_states = {state_mapping[state] for state in self.afd_accept_states}

        return new_states, self.afd_symbols, new_transitions, new_start_state, new_accept_states
    
    """
    Simulate the minimized AFD
    :param input_chain: Input chain
    Simula el AFD minimizado con una cadena de entrada y devuelve si la cadena es aceptada
    """
    def simulate_minafd(self, input_chain):
        # Start from the minDFA's start state
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

"""
Minimize an AFD
:param afd_states: States, afd_symbols, afd_transitions: Transitions, afd_start_state: Start state, afd_accept_states: Accept states
Crea una instancia de DFAMinimizer y minimiza el AFD
"""
def minimize_afd(afd_states, afd_symbols, afd_transitions, afd_start_state, afd_accept_states):
    dfa_minimizer = DFAMinimizer(
        afd_states, 
        afd_symbols, 
        afd_transitions, 
        afd_start_state, 
        afd_accept_states
    )
    minimized_afd = dfa_minimizer.minimize()
    return minimized_afd

"""
Visualize the minimized AFD
:param states: States, symbols: Symbols, transitions: Transitions, start_state: Start state, accept_states: Accept states
Crea un gráfico del AFD minimizado
"""
def visualize_minimized_afd(states, symbols, transitions, start_state, accept_states):
    graph = Digraph(format='png', graph_attr={'rankdir': 'LR'})
    
    # Create mapping for states to letters
    state_to_number = {state: chr(ord('1') + i) for i, state in enumerate(states)}
    
    graph.attr('node', shape='none', width='0', height='0')
    graph.node('start', label='', shape='none')
    graph.edge('start', str(start_state), arrowhead='vee')
    
    for state, letter in state_to_number.items():
        shape = 'doublecircle' if state in accept_states else 'circle'
        graph.node(str(state), label=letter, shape=shape)

    for (from_state, symbol), to_state in transitions.items():
        graph.edge(str(from_state), str(to_state), label=symbol)

    graph.render('minimized_afd')

# programmed by @melissaperez_
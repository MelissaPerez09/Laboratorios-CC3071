"""
MinAFD.py
Minimization of and AFD
"""

from graphviz import Digraph

class DFAMinimizer:
    def __init__(self, afd_states, afd_symbols, afd_transitions, afd_start_state, afd_accept_states):
        self.afd_states = list(afd_states)
        self.afd_symbols = list(afd_symbols)
        self.afd_transitions = afd_transitions
        self.afd_start_state = afd_start_state
        self.afd_accept_states = set(afd_accept_states)

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


"""
finalAutomata.py
Grafica los autómatas finitos deterministas y los une en un autómata finito no determinista
"""

from graphviz import Digraph

class DFAUnion:
    def __init__(self):
        self.dfas = []

    def add_dfa(self, dfa_transitions, start_state, accept_states):
        assert isinstance(dfa_transitions, dict)
        for state, transitions in dfa_transitions.items():
            assert isinstance(transitions, dict)
        self.dfas.append((dfa_transitions, start_state, accept_states))

    def union(self):
        afnd_transitions = {}
        afnd_start_state = 'q0'
        afnd_accept_states = set()
        afnd_transitions[afnd_start_state] = {}

        for dfa_transitions, start_state, accept_states in self.dfas:
            if None not in afnd_transitions[afnd_start_state]:
                afnd_transitions[afnd_start_state][None] = set()
            afnd_transitions[afnd_start_state][None].add(start_state)
            
            for state, transitions in dfa_transitions.items():
                if state not in afnd_transitions:
                    afnd_transitions[state] = {}
                for symbol, next_states in transitions.items():
                    if symbol not in afnd_transitions[state]:
                        afnd_transitions[state][symbol] = set()
                    afnd_transitions[state][symbol].update(next_states)

            afnd_accept_states.update(accept_states)

        return afnd_transitions, afnd_start_state, afnd_accept_states

    
def draw_afnd(transitions, start_state, accept_states):
    graph = Digraph(format='png')

    for state in transitions.keys():
        graph.node(str(state), str(state))
        for symbol, next_states in transitions[state].items():
            for next_state in next_states:
                graph.edge(str(state), str(next_state), label=str(symbol) if symbol else 'ε')
    for accept_state in accept_states:
        graph.node(str(accept_state), shape='doublecircle')

    graph.render('afnd', view=False)

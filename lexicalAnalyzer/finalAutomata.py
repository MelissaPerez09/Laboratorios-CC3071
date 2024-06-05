"""
finalAutomata.py
Grafica los autómatas finitos deterministas y los une en un autómata finito no determinista
"""

from graphviz import Digraph

class DFAUnion:
    def __init__(self):
        self.dfas = []

    """
    Agrega un DFA a la unión
    :param dfa_transitions: Transiciones del DFA
    :param start_state: Estado inicial
    :param accept_states: Estados de aceptación
    :param token_action: Acción del token
    """
    def add_dfa(self, dfa_transitions, start_state, accept_states, token_action):
        self.dfas.append((dfa_transitions, start_state, accept_states, token_action))

    """
    Une los DFAs en un AFND
    returns las transiciones, estado inicial, estados de aceptación y acciones de token del AFND
    """
    def union(self):
        afnd_transitions = {}
        afnd_start_state = 'start'
        afnd_accept_states = set()
        token_actions = {}
        afnd_transitions[afnd_start_state] = {}

        for dfa_transitions, start_state, accept_states, token_action in self.dfas:
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
            for accept_state in accept_states:
                token_actions[accept_state] = token_action

        return afnd_transitions, afnd_start_state, afnd_accept_states, token_actions

"""
Dibuja un DFA
:param transitions: Transiciones del DFA
:param start_state: Estado inicial
:param accept_states: Estados de aceptación
"""    
def draw_afnd(transitions, start_state, accept_states, token_actions):
    graph = Digraph(format='png')

    for state in transitions.keys():
        if state in accept_states:
            token_action = token_actions.get(state, '')
            graph.node(str(state), f'{str(state)}\n{token_action}', shape='doublecircle')
        else:
            graph.node(str(state), str(state))

        for symbol, next_states in transitions[state].items():
            for next_state in next_states:
                graph.edge(str(state), str(next_state), label=str(symbol) if symbol else 'ε')
    
    MAX_LABEL_LENGTH = 100

    def truncate_label(label):
        return (label[:MAX_LABEL_LENGTH] + '..') if len(label) > MAX_LABEL_LENGTH else label

    for accept_state in accept_states:
        token_action = token_actions.get(accept_state, '')
        token_action = truncate_label(token_action)
        print(f'Accept State: {accept_state}, Token Action: {token_action}')
        graph.node(str(accept_state), f'{str(accept_state)}\n{token_action}', shape='doublecircle')


    graph.render('afnd', view=True)

# programmed by @melissaperez_
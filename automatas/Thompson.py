"""
Thompson.py
Uses McNaughton–Yamada–Thompson algorithm to convert postfix expression to NFA
"""

from graphviz import Digraph

class Thompson:
    def __init__(self):
        self.epsilon = "ε"
    
    """
    Convert postfix expression to NFA
    :param postfix_expression: Postfix expression
    Guarda los estados, transiciones y simbolos de la expresion regular
    """
    def convert2NFA(self, postfix_expression):
        regex = postfix_expression

        keys = list(set([char for char in regex if char.isalnum()] + list(self.epsilon)))

        states = []
        stack = []
        counter = 0

        for i in regex:
            if i in keys:  # Terminal symbol
                c1 = counter
                counter += 1
                c2 = counter
                counter += 1
                states.append({})
                states.append({})
                stack.append([c1, c2])
                states[c1][i] = c2
            elif i == '*':  # Kleene star
                r1, r2 = stack.pop()
                c1 = counter
                counter += 1
                c2 = counter
                counter += 1
                states.append({})
                states.append({})
                stack.append([c1, c2])
                states[r2][self.epsilon] = (r1, c2)
                states[c1][self.epsilon] = (r1, c2)
            elif i == ".":  # Concatenation
                r21, r22 = stack.pop()
                r11, r12 = stack.pop()
                stack.append([r11, r22])
                states[r12][self.epsilon] = r21
            elif i == "|":  # Union
                c1 = counter
                counter += 1
                c2 = counter
                counter += 1
                states.append({})
                states.append({})
                r11, r12 = stack.pop()
                r21, r22 = stack.pop()
                stack.append([c1, c2])
                states[c1][self.epsilon] = (r21, r11)
                states[r12][self.epsilon] = c2
                states[r22][self.epsilon] = c2

        start, end = stack.pop()
        # Re-index states
        new_states = [{} for _ in range(len(states))]
        state_mapping = {old: new for new, old in enumerate(sorted(range(len(states)), key=lambda x: (x != start, x)))}
        for old_state, transitions in enumerate(states):
            for symbol, next_states in transitions.items():
                if isinstance(next_states, tuple):
                    new_states[state_mapping[old_state]][symbol] = tuple(state_mapping[s] for s in next_states)
                else:
                    new_states[state_mapping[old_state]][symbol] = state_mapping[next_states]

        return (keys, new_states, state_mapping[start], state_mapping[end])
    
    """
    Get formatted AFN parameters
    :param afn: AFN tuple
    Convierte el estado final en un conjunto, 
    genera una lista de estados basada en las transiciones 
    y reformatea las transiciones para que cada estado tenga una 
    lista de estados siguientes para cada símbolo
    """
    def get_formatted_afn_params(self, afn: tuple) -> tuple:
        nfa_symbols, nfa_og_transitions, nfa_start, nfa_end = afn
        nfa_end = {nfa_end} # Convert end state to a set
        nfa_states = [i for i in range(len(nfa_og_transitions))]
        nfa_transitions = {}
        for i in range(len(nfa_og_transitions)):
            if isinstance(nfa_og_transitions[i], dict):
                new_transition = {}
                for symbol in nfa_symbols:
                    if isinstance(nfa_og_transitions[i].get(symbol), (tuple, list)):
                        next_states = nfa_og_transitions[i].get(symbol)
                    elif nfa_og_transitions[i].get(symbol) is not None:
                        next_states = [nfa_og_transitions[i].get(symbol)]
                    else:
                        next_states = []
                    new_transition[symbol] = next_states
                nfa_transitions[i] = new_transition
        return nfa_symbols, nfa_states, nfa_transitions, nfa_start, nfa_end

    """
    Epsilon Closure
    :param states: Set of states
    Calcula el cierre epsilon de un conjunto de estados
    """
    def epsilon_closure(self, states, nfa_transitions):
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            epsilon_transitions = nfa_transitions.get(state, {}).get(self.epsilon, [])
            for next_state in epsilon_transitions:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

    """
    Graph NFA
    :param nfa
    Crea un nodo para cada estado y una arista para cada transición
    """
    def graph_nfa(self, nfa):
        nfa_symbols, nfa_states, nfa_transitions, nfa_start, nfa_end = self.get_formatted_afn_params(nfa)

        f = Digraph('finite_state_machine', filename='nfa.gv')
        f.attr(rankdir='LR', size='8,5')

        f.attr('node', shape='doublecircle')
        for final_state in nfa_end:
            f.node(str(final_state))

        f.attr('node', shape='circle')
        for state in nfa_states:
            if state not in nfa_end:
                f.node(str(state))

        # Add an invisible node for the start arrow
        f.attr('node', shape='none', width='0', height='0')
        f.node('start')

        # Add an edge from the invisible node to the start state
        f.edge('start', str(nfa_start), color='black')

        # Sort transitions by the minimum reachable state
        sorted_transitions = sorted(nfa_transitions.items(), key=lambda t: min(min(v) if isinstance(v, (tuple, list)) else v for v in t[1]) if t[1] else 0)

        for state, transitions in sorted_transitions:
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    f.edge(str(state), str(next_state), label=symbol)

        f.render(filename='nfa', format='png', cleanup=True)

    """
    Simulate NFA
    :param nfa: NFA tuple
    simula la ejecución de un NFA en una cadena de entrada y verifica si la cadena es aceptada
    """
    def simulate_nfa(self, nfa, input_chain):
        _, nfa_states, nfa_transitions, nfa_start, nfa_end = self.get_formatted_afn_params(nfa)

        current_states = self.epsilon_closure({nfa_start}, nfa_transitions)

        for symbol in input_chain:
            next_states = set()
            for state in current_states:
                if symbol in nfa_transitions[state]:
                    for next_state in nfa_transitions[state][symbol]:
                        next_states.update(self.epsilon_closure({next_state}, nfa_transitions))
            current_states = next_states
        
        return bool(current_states & nfa_end)
    
# programmed by @melissaperez_
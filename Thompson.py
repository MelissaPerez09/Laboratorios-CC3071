"""
Thompson.py
Uses McNaughton–Yamada–Thompson algorithm to convert postfix expression to NFA
"""
import re
from graphviz import Digraph

class Thompson:
    def __init__(self, epsilon, concat_operator="."):
        self.epsilon = epsilon
        self.concat_operator = concat_operator
        
    def convert2NFA(self, postfix_expression):
        regex = postfix_expression

        keys = list(set(re.sub('[^A-Za-z0-9]+', '', regex) + self.epsilon))

        states = []
        stack = []
        counter = -1

        for i in regex:
            if i in keys:                   # Terminal symbol
                counter += 1
                c1 = counter
                counter += 1
                c2 = counter
                states.append({})
                states.append({})
                stack.append([c1, c2])
                states[c1][i] = c2
            elif i == '*':                  # Kleen star
                r1, r2 = stack.pop()
                counter += 1
                c1 = counter
                counter += 1
                c2 = counter
                states.append({})
                states.append({})
                stack.append([c1, c2])
                states[r2][self.epsilon] = (r1, c2)
                states[c1][self.epsilon] = (r1, c2)
            elif i == self.concat_operator: # Concatenation
                r21, r22 = stack.pop()
                r11, r12 = stack.pop()
                stack.append([r11, r22])
                states[r12][self.epsilon] = r21
            elif i == "+":                  # Union
                counter += 1
                c1 = counter
                counter += 1
                c2 = counter
                states.append({})
                states.append({})
                r11, r12 = stack.pop()
                r21, r22 = stack.pop()
                stack.append([c1, c2])
                states[c1][self.epsilon] = (r21, r11)
                states[r12][self.epsilon] = c2
                states[r22][self.epsilon] = c2

        start, end = stack.pop()
        return (keys, states, start, end)
    
    def get_formatted_afn_params(self, afn: tuple) -> tuple:
        nfa_symbols, nfa_og_transitions, nfa_start, nfa_end = afn
        nfa_end = {nfa_end} # Convert end state to a set
        nfa_states = [i for i in range(len(nfa_og_transitions))]
        nfa_transitions = {}
        for i in range(len(nfa_og_transitions)):
            new_transition = {}
            for symbol in nfa_symbols:
                if nfa_og_transitions[i].get(symbol) is not None:
                    next_states = nfa_og_transitions[i].get(symbol)
                    new_transition[symbol] = [next_states] if not isinstance(next_states, tuple) else list(next_states)
            nfa_transitions[i] = new_transition
            
        return (nfa_symbols, nfa_states, nfa_transitions, nfa_start, nfa_end)
    
    from graphviz import Digraph

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

        # Add an edge from the invisible node to state 0
        f.edge('start', '0', color='white')

        # Ensure that state 0 is the first transition
        if 0 in nfa_transitions:
            for symbol, next_states in nfa_transitions[0].items():
                for next_state in next_states:
                    f.edge(str(0), str(next_state), label=symbol)

        for state, transitions in nfa_transitions.items():
            if state != 0:
                for symbol, next_states in transitions.items():
                    for next_state in next_states:
                        f.edge(str(state), str(next_state), label=symbol)

        f.render(filename='nfa', format='png', cleanup=True)
    
    def process_input(self, input_strings, nfa):
        keys, states, start, end = nfa
        for input_string in input_strings:
            current_states = {start}  # Initially, the current state is the start state
            current_states = self.epsilon_closure(current_states, states)
            for symbol in input_string:
                next_states = set()
                for state in current_states:
                    if symbol in states[state]:
                        transition = states[state][symbol]
                        if isinstance(transition, tuple):
                            next_states.update(transition)
                        else:
                            next_states.add(transition)
                current_states = self.epsilon_closure(next_states, states)
            # After processing the string, check if the current state is in the accept state
            if end in current_states:
                print(f"'{input_string}' is accepted")
            else:
                print(f"'{input_string}' is not accepted")
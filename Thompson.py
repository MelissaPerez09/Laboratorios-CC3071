"""
Thompson.py
Uses McNaughton–Yamada–Thompson algorithm to convert postfix expression to NFA
"""
import re
from graphviz import Digraph

class Thompson:
    def __init__(self):
        self.epsilon = "ε"
        
    def convert2NFA(self, postfix_expression):
        regex = postfix_expression

        keys = list(set(re.sub('[^A-Za-z0-9]+', '', regex) + self.epsilon))

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
            """
            elif i == '+':  # One or more
                r1, r2 = stack.pop()
                c1 = counter
                counter += 1
                states.append({})
                stack.append([r1, c1])
                states[r2][self.epsilon] = (r1, c1)
            elif i == '?':  # Zero or one
                r1, r2 = stack.pop()
                c1 = counter
                counter += 1
                c2 = counter
                counter += 1
                states.append({})
                states.append({})
                stack.append([c1, c2])
                states[c1][self.epsilon] = (r1, c2)
                states[r2][self.epsilon] = c2
            """

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
        sorted_transitions = sorted(nfa_transitions.items(), key=lambda t: min(min(v) if isinstance(v, (tuple, list)) else v for v in t[1].values()) if t[1].values() else 0)

        for state, transitions in sorted_transitions:
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
"""
gammar.py
Define la estructura de la gramática utilizada por el analizador sintáctico
"""

import sys
sys.path.insert(0, '/Users/melissa/Desktop/UVG/lenguajes/CC3071-LabAB/')

from lexicalAnalyzer.yalexParser import YALexParser

class YAParParser:
    def __init__(self, yapar_path):
        self.yapar_path = yapar_path
    
    def parse(self):
        grammar = {}
        tokens = set()
        
        with open(self.yapar_path, 'r') as file:
            content = file.readlines()
        
        current_section = None
        current_head = None
        for line in content:
            line = line.strip()
            if line.startswith('/*') and line.endswith('*/'):
                continue
            elif line.startswith('%token'):
                parts = line.split()
                tokens.update(parts[1:])
            elif line.startswith('%%'):
                current_section = 'rules'
            elif current_section == 'rules' and line:
                if line.endswith(';'):
                    line = line[:-1]
                if ':' in line:
                    head, production = line.split(':')
                    head = head.strip()
                    current_head = head
                    grammar[current_head] = []
                    line = production
                if current_head:
                    productions = [prod.strip() for prod in line.split('|')]
                    for prod in productions:
                        if prod:
                            production = tuple(prod.split())
                            grammar[current_head].append(production)
            elif line.startswith('IGNORE'):
                _, ignore_token = line.split()
                if ignore_token in tokens:
                    tokens.remove(ignore_token)
                    
        self.grammar = grammar
        self.tokens = tokens

    def print_grammar(self):
        for nonterminal, productions in self.grammar.items():
            print(f"{nonterminal} -> {[' '.join(prod) for prod in productions]}")

class AutomataLR0:
    def __init__(self, grammar):
        self.grammar = grammar
        self.states = []
        self.transitions = {}
        self.start_symbol = None
        self.end_symbol = "$"

    # Añade un símbolo de fin de cadena a la gramática.
    def augment_grammar(self):
        self.start_symbol = 'S'
        self.grammar[self.start_symbol] = [(next(iter(self.grammar.keys())), self.end_symbol)]

    # Calcula la cerradura de un conjunto de elementos.
    def closure(self, items):
        closure_set = set(items)

        while True:
            new_items = set()
            for item in closure_set:
                # Asume que item es una tupla (head, body, dot_position)
                head, body, dot_position = item
                if dot_position < len(body) and body[dot_position] in self.grammar:
                    next_symbol = body[dot_position]
                    for production in self.grammar[next_symbol]:
                        new_item = (next_symbol, production, 0)
                        if new_item not in closure_set:
                            new_items.add(new_item)

            if not new_items:
                break

            closure_set.update(new_items)

        return closure_set

    # Determina el estado al que se llega desde un estado dado por un símbolo.
    def goto(self, state, symbol):
        new_state = set()
        for item in state:
            head, body, dot_position = item
            if dot_position < len(body) and body[dot_position] == symbol:
                new_item = (head, body, dot_position + 1)
                new_state.add(new_item)
        return self.closure(new_state)

    # Construye el conjunto de elementos para la gramática.
    def items(self):
        initial_item = (self.start_symbol, self.grammar[self.start_symbol][0], 0)
        initial_state = self.closure({initial_item})
        states = [initial_state]

        while True:
            new_states = []
            for state in states:
                for symbol in self.grammar.keys():
                    next_state = self.goto(state, symbol)
                    if next_state and next_state not in states and next_state not in new_states:
                        new_states.append(next_state)

            if not new_states:
                break

            states.extend(new_states)

        return states

    # Construye todos los estados del autómata LR(0).
    def build_states(self):
        self.states = self.items()

    # Define las transiciones entre los estados basados en los símbolos de la gramática.
    def build_transitions(self):
        self.transitions = {}
        for i, state in enumerate(self.states):
            self.transitions[i] = {}
            for symbol in self.grammar.keys():
                next_state = self.goto(state, symbol)
                if next_state in self.states:
                    self.transitions[i][symbol] = self.states.index(next_state)

    # Determina las acciones de análisis para cada estado (shift, reduce, accept, error).
    def parsing_actions(self):
        self.actions = {}
        for i, state in enumerate(self.states):
            self.actions[i] = {}
            for item in state:
                head, body, dot_position = item
                if dot_position == len(body):  # Reduce
                    for symbol in self.grammar.keys():
                        if symbol != self.start_symbol:
                            self.actions[i][symbol] = ('reduce', head)
                elif body[dot_position] in self.grammar:  # Shift
                    next_state = self.goto(state, body[dot_position])
                    if next_state in self.states:
                        self.actions[i][body[dot_position]] = ('shift', self.states.index(next_state))
                elif body[dot_position] == '':  # Accept
                    self.actions[i][''] = ('accept', )

            
def extract_token_names(yalex_tokens):
    # Extraer solo las claves que contienen nombres de tokens desde las acciones de YALex
    return {token.split()[1].strip("'") for token in yalex_tokens.keys() if token.strip()}

def validate_tokens(yapar_tokens, yalex_tokens):
    yalex_token_names = extract_token_names(yalex_tokens)
    missing_in_yalex = yapar_tokens - yalex_token_names
    missing_in_yapar = yalex_token_names - yapar_tokens
    
    if missing_in_yalex:
        print("Tokens missing in YALex:", missing_in_yalex)
    if missing_in_yapar:
        print("Tokens missing in YAPar:", missing_in_yapar)
    
    return not missing_in_yalex and not missing_in_yapar

# Paths to the files
yapar_path = './yapar/slr-1.yalp'
yalex_path = './yalex/slr-1.yal'

# Parsing YAPar and YALex
yapar_parser = YAParParser(yapar_path)
yapar_parser.parse()
yapar_parser.print_grammar()

yalex_parser = YALexParser(yalex_path)
yalex_parser.parse()
yalex_tokens = yalex_parser.generate_all_regex()

# Token Validation
is_valid = validate_tokens(yapar_parser.tokens, yalex_tokens)
print("Validation Successful:", is_valid)

automata = AutomataLR0(yapar_parser.grammar)
automata.augment_grammar()
automata.build_states()
automata.build_transitions()
automata.parsing_actions()

print("\nStates:")
for i, state in enumerate(automata.states):
    print(f"State {i}:")
    for item in state:
        head, body, dot_position = item
        body_with_dot = list(body[:dot_position]) + ['•'] + list(body[dot_position:])
        print(f"  {head} -> {' '.join(body_with_dot)}")
    print()

print("Transitions:")
for i, transitions in automata.transitions.items():
    for symbol, next_state in transitions.items():
        print(f"From state {i} on symbol {symbol} go to state {next_state}")
print()

print("Parsing actions:")
for i, actions in automata.actions.items():
    for symbol, action in actions.items():
        print(f"In state {i} on symbol {symbol} do {action}")

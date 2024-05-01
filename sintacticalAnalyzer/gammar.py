"""
gammar.py
Define la estructura de la gramática utilizada por el analizador sintáctico
"""

import sys
import graphviz
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
        print("\n----------------------------\nDetected grammar:\n----------------------------")
        for nonterminal, productions in self.grammar.items():
            print(f"{nonterminal} -> {[' '.join(prod) for prod in productions]}")

class AutomataLR0:
    def __init__(self, grammar, tokens):
        self.grammar = grammar
        self.tokens = tokens
        self.start_symbol = None
        self.states = []
        self.transitions = {}
        self.actions = {}
        self.augment_grammar()

    def augment_grammar(self):
        self.start_symbol = 'S\''
        original_start_symbol = next(iter(self.grammar))
        self.grammar[self.start_symbol] = [(original_start_symbol, '$')]

    def closure(self, items):
        closure_set = set(items)
        while True:
            new_items = set()
            for (head, body, dot_position) in closure_set:
                if dot_position < len(body):
                    symbol = body[dot_position]
                    if symbol in self.grammar:
                        for prod in self.grammar[symbol]:
                            new_item = (symbol, prod, 0)
                            if new_item not in closure_set:
                                new_items.add(new_item)
            if not new_items:
                break
            closure_set |= new_items
        return closure_set

    def goto(self, state, symbol):
        new_state = set()
        for (head, body, dot_position) in state:
            if dot_position < len(body) and body[dot_position] == symbol:
                new_state.add((head, body, dot_position + 1))
        return self.closure(new_state)

    def build_states(self):
        initial_item = (self.start_symbol, self.grammar[self.start_symbol][0], 0)
        initial_state = self.closure({initial_item})
        self.states = [initial_state]
        transitions = {}

        while True:
            new_states = False
            for state in list(self.states):
                for symbol in self.grammar.keys() | self.tokens | {'$'}:
                    next_state = self.goto(state, symbol)
                    if next_state and next_state not in self.states:
                        self.states.append(next_state)
                        new_states = True
                    if next_state:
                        transitions[(tuple(state), symbol)] = next_state
            if not new_states:
                break

        self.transitions = {k: self.states.index(v) for k, v in transitions.items()}

    def parsing_actions(self):
        for state_index, state in enumerate(self.states):
            for item in state:
                head, body, dot_position = item
                if dot_position == len(body):  # We are at the end of a production.
                    if head == self.start_symbol:  # Accept condition.
                        self.actions[(state_index, '$')] = ('accept', None)
                    else:
                        for prod_index, prod in enumerate(self.grammar[head]):
                            if prod == body:
                                self.actions[(state_index, symbol)] = ('reduce', prod_index)
                else:
                    symbol = body[dot_position]
                    if symbol in self.tokens:  # Shift condition.
                        next_state = self.transitions[(tuple(state), symbol)]
                        self.actions[(state_index, symbol)] = ('shift', next_state)

            
def extract_token_names(yalex_tokens):
    token_names = set()
    for token in yalex_tokens.keys():
        if token.strip():
            # Extract token name from print or return statement
            start_quote = token.find("'") if token.find("'") != -1 else token.find('"')
            end_quote = token.rfind("'") if token.rfind("'") != -1 else token.rfind('"')
            if start_quote != -1 and end_quote != -1 and start_quote != end_quote:
                token_name = token[start_quote + 1:end_quote]
                token_names.add(token_name)
            else:
                print(f"Warning: Token '{token}' does not contain a valid token name")
    return token_names

def validate_tokens(yapar_tokens, yalex_tokens):
    yalex_token_names = extract_token_names(yalex_tokens)
    missing_tokens = yapar_tokens - yalex_token_names
    if missing_tokens:
        return False, missing_tokens
    else:
        return True, None

def generate_automata_graph(automata, filename):
    dot = graphviz.Digraph(format='png')

    for i, state in enumerate(automata.states):
        label = ""
        for (head, body, dot_position) in state:
            if head == "S'" and dot_position == len(body):
                label = "ACCEPT"
                break
            else:
                body_with_dot = body[:dot_position] + ('•',) + body[dot_position:]
                label += f"  {head} -> {' '.join(body_with_dot)}\n"
        dot.node(str(i), label if label != "ACCEPT" else "ACCEPT", shape='box')

    for (state, symbol), next_state in sorted(automata.transitions.items()):
        dot.edge(str(state_to_index[tuple(state)]), str(next_state), label=symbol)

    dot.node("start", "", shape="none", width="0", height="0")
    dot.edge("start", "0", shape="none")

    dot.render(filename)

# Paths to the files
yapar_path = './yapar/slr-8.yalp'
yalex_path = './yalex/slr-1.yal'

# Parsing YAPar and YALex
yapar_parser = YAParParser(yapar_path)
yapar_parser.parse()
yapar_parser.print_grammar()

yalex_parser = YALexParser(yalex_path)
yalex_parser.parse()
yalex_tokens = yalex_parser.generate_all_regex()

# Token Validation
is_valid, missing_tokens = validate_tokens(yapar_parser.tokens, yalex_tokens)
if not is_valid:
    print(f"\n----------------------------\nToken validation: False\n----------------------------")
    print(f"(!)ERROR, Tokens missing: {missing_tokens}")
    exit(1)
print(f"\n----------------------------\nToken validation: True\n----------------------------")

automata = AutomataLR0(yapar_parser.grammar, yapar_parser.tokens)
automata.build_states()
automata.parsing_actions()

print("\n----------------------------\nStates:\n----------------------------")
for i, state in enumerate(automata.states):
    print(f"I{i}:")
    for (head, body, dot_position) in state:
        body_with_dot = body[:dot_position] + ('•',) + body[dot_position:]
        print(f"  {head} -> {' '.join(body_with_dot)}")
    print()

print("----------------------------\nTransitions:\n----------------------------")
state_to_index = {tuple(state): index for index, state in enumerate(automata.states)}
for (state, symbol), next_state in sorted(automata.transitions.items()):
    print(f"From I{state_to_index[tuple(state)]} with '{symbol}' to I{next_state}")
print()

generate_automata_graph(automata, 'automataLR(0)')
"""
gammarUI.py
Define la estructura de la gramática utilizada por el analizador sintáctico
Se utiliza en la interfaz gráfica
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
        dot.edge(str(i), str(next_state), label=symbol)

    dot.node("start", "", shape="none", width="0", height="0")
    dot.edge("start", "0", shape="none")

    dot.render(filename)

def first(grammar, symbol, first_sets):
    if symbol in first_sets:
        return first_sets[symbol]

    first_result = set()
    if symbol not in grammar:
        first_result.add(symbol)
    else:
        for production in grammar[symbol]:
            prod_symbols = production if isinstance(production, tuple) else production.split()
            for prod_symbol in prod_symbols:
                if prod_symbol == symbol:
                    break
                temp_first = first(grammar, prod_symbol, first_sets)
                first_result.update(temp_first - {''})
                if '' not in temp_first:
                    break
            else:
                first_result.add('')
    first_sets[symbol] = first_result
    return first_result

def follow(grammar, symbol, follow_sets, first_sets):
    if symbol not in follow_sets:
        follow_sets[symbol] = set()
        if symbol == next(iter(grammar)):
            follow_sets[symbol].add('$')

    for head, productions in grammar.items():
        for production in productions:
            production_parts = production if isinstance(production, tuple) else production.split()
            for i, part in enumerate(production_parts):
                if part == symbol:
                    next_symbols = production_parts[i+1:]
                    if next_symbols:
                        next_first = set()
                        derives_empty = False
                        for ns in next_symbols:
                            temp_first = first(grammar, ns, first_sets)
                            next_first.update(temp_first - {'ε'})
                            if 'ε' in temp_first:
                                derives_empty = True
                                continue
                            else:
                                break
                        if derives_empty:
                            follow_sets[symbol].update(follow_sets[head])
                        follow_sets[symbol].update(next_first)
                    else:
                        if head != symbol:
                            follow(grammar, head, follow_sets, first_sets)
                            follow_sets[symbol].update(follow_sets[head])

def compute_sets(grammar):
    first_sets = {}
    follow_sets = {}
    for nonterminal in grammar:
        first(grammar, nonterminal, first_sets)
    for nonterminal in grammar:
        follow(grammar, nonterminal, follow_sets, first_sets)
    return first_sets, follow_sets
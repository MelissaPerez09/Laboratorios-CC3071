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
    
    """
    Parsea el archivo YAPar para obtener la gramática y los tokens
    """
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

    """
    Imprime la gramática y los tokens
    """
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

    """
    Agrega un símbolo inicial a la gramática
    """
    def augment_grammar(self):
        self.start_symbol = 'S\''
        original_start_symbol = next(iter(self.grammar))
        self.grammar[self.start_symbol] = [(original_start_symbol, '$')]

    """
    Calcula el cierre de un conjunto de ítems (función CERRADURA)
    """
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

    """
    Calcula el conjunto de ítems al que se llega desde un estado con un símbolo dado (función IR_A)
    """
    def goto(self, state, symbol):
        new_state = set()
        for (head, body, dot_position) in state:
            if dot_position < len(body) and body[dot_position] == symbol:
                new_state.add((head, body, dot_position + 1))
        return self.closure(new_state)

    """
    Construye los estados del autómata LR(0)
    """
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

    """
    Calcula las acciones de la tabla de análisis sintáctico
    """
    def parsing_actions(self):
        for state_index, state in enumerate(self.states):
            for item in state:
                head, body, dot_position = item
                if dot_position == len(body):
                    if head == self.start_symbol:
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

"""
Extrae los nombres de los tokens de un diccionario de tokens de YALex
"""
def extract_token_names(yalex_tokens):
    token_names = set()
    for token in yalex_tokens.keys():
        if token.strip():
            start_quote = token.find("'") if token.find("'") != -1 else token.find('"')
            end_quote = token.rfind("'") if token.rfind("'") != -1 else token.rfind('"')
            if start_quote != -1 and end_quote != -1 and start_quote != end_quote:
                token_name = token[start_quote + 1:end_quote]
                token_names.add(token_name)
            else:
                print(f"Warning: Token '{token}' does not contain a valid token name")
    return token_names

"""
Valida que los tokens de YAPar estén contenidos en los tokens de YALex
"""
def validate_tokens(yapar_tokens, yalex_tokens):
    yalex_token_names = extract_token_names(yalex_tokens)
    missing_tokens = yapar_tokens - yalex_token_names
    if missing_tokens:
        return False, missing_tokens
    else:
        return True, None

"""
Genera el grafo del autómata LR(0)
Identifica los que pertenecen al corazón y los que no
"""
def generate_automata_graph(automata, filename):
    dot = graphviz.Digraph(format='png')
    added_transitions = set()

    state_to_index = {tuple(state): index for index, state in enumerate(automata.states)}

    for i, state in enumerate(automata.states):
        accept_state = False
        for (head, body, dot_position) in state:
            if head == "S'" and body[-1] == '$' and dot_position == len(body):
                accept_state = True
                break

        if accept_state:
            label = 'ACCEPT'
        else:
            label = f"I{i}:\n"
            heart_productions = []
            body_productions = []

            for (head, body, dot_position) in state:
                body_with_dot = body[:dot_position] + ('•',) + body[dot_position:]
                production_label = f"{head} -> {' '.join(body_with_dot)}"

                if (head == "S'" and dot_position == 0) or dot_position != 0:
                    heart_productions.append(production_label)
                else:
                    body_productions.append(production_label)

            if heart_productions:
                label += "HEART:\n" + "\n".join(heart_productions) + "\n"
            if body_productions:
                label += "\nBODY:\n" + "\n".join(body_productions)

        dot.node(f"I{i}", label, shape='box')

    for (state, symbol), next_state in sorted(automata.transitions.items()):
        from_index = state_to_index[tuple(state)]
        if (from_index, symbol, next_state) not in added_transitions:
            dot.edge(f"I{from_index}", f"I{next_state}", label=symbol)
            added_transitions.add((from_index, symbol, next_state))

    dot.node("start", "", shape="none", width="0", height="0")
    dot.edge("start", "I0", shape="none")

    dot.render(filename)
    
# programmed by @melissaperez_
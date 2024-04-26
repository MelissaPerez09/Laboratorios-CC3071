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

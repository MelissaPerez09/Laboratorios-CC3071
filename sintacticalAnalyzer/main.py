"""
main.py
Sintactial Analyzer Main, no UI
"""

import sys
sys.path.insert(0, '/Users/melissa/Desktop/UVG/lenguajes/CC3071-LabAB/')

from lexicalAnalyzer.yalexParser import YALexParser
from sintacticalAnalyzer.gammar import *
from sintacticalAnalyzer.functions import *

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
    heart_productions = []
    body_productions = []

    for (head, body, dot_position) in state:
        body_with_dot = body[:dot_position] + ('•',) + body[dot_position:]
        production_string = f"  {head} -> {' '.join(body_with_dot)}"

        # Determine if it is a Heart or Body element
        if (head == "S'" and dot_position == 0) or dot_position != 0:
            heart_productions.append(production_string)
        else:
            body_productions.append(production_string)

    if heart_productions:
        print("HEART:")
        for production in heart_productions:
            print(production)
    if body_productions:
        print("BODY:")
        for production in body_productions:
            print(production)
    print()

print("----------------------------\nTransitions:\n----------------------------")
state_to_index = {tuple(state): index for index, state in enumerate(automata.states)}
for (state, symbol), next_state in sorted(automata.transitions.items()):
    print(f"From I{state_to_index[tuple(state)]} with '{symbol}' to I{next_state}")
print()

generate_automata_graph(automata, 'automataLR(0)')

first_sets, follow_sets = compute_sets(yapar_parser.grammar)
print("FIRST sets:", first_sets)
print("FOLLOW sets:", follow_sets)
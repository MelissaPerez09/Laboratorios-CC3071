"""
LexSyn.py
Une el analizador léxico y sintáctico completo
"""

import sys
sys.path.insert(0, '/Users/melissa/Desktop/UVG/lenguajes/CC3071-LabAB/')

from lexicalAnalyzer.yalexParser import YALexParser
from lexicalAnalyzer.LexicalAnalyzer import *
from sintacticalAnalyzer.gammar import *
from sintacticalAnalyzer.SRLTable import *
from sintacticalAnalyzer.parser import *

def LexSyn(yalex_path, yapar_path, chars_path):
    # Archivo de entrada
    yalex_parser = YALexParser(yalex_path)
    yalex_parser.parse()
    regex_tokens = yalex_parser.generate_all_regex()

    yapar_parser = YAParParser(yapar_path)
    yapar_parser.parse()
    yapar_parser.print_grammar()
    grammar_rules = generate_grammar_rules(yapar_parser.grammar)

    """
    Análisis Léxico
    """
    # Generación de lo estados y construcción de autómatas
    dfa_union = DFAUnion()
    for token, regex in regex_tokens.items():
        dfa_transitions, start_state, accept_states = applyDirect(regex)
        draw_dfa(dfa_transitions, start_state, accept_states)
        converted_transitions = convert_transitions(dfa_transitions)
        dfa_union.add_dfa(converted_transitions, start_state, accept_states, token)

    # Realizar la unión de DFAs
    afnd_transitions, afnd_start_state, afnd_accept_states, token_actions = dfa_union.union()
    draw_afnd(afnd_transitions, afnd_start_state, afnd_accept_states, token_actions)
    
    tokens, lexical_errors = analizar_archivo(afnd_transitions, afnd_start_state, token_actions, chars_path)
    
    if lexical_errors:
        print("Se encontraron errores léxicos:")
        for error in lexical_errors:
            print(f'Error léxico en línea {error[0]}, posición {error[1]}: {error[2]}')
        return
    
    """
    Análisis Sintáctico
    """
    # Construcción del autómata LR(0)
    automata = AutomataLR0(yapar_parser.grammar, yapar_parser.tokens)
    automata.build_states()
    automata.parsing_actions()
    generate_automata_graph(automata, "automataLR(0)")

    # Construcción de la tabla de análisis sintáctico SLR
    actions, gotos = automata.parsing_table()
    print_parsing_table(actions, gotos, yapar_parser.tokens, yapar_parser.grammar.keys(), len(automata.states), grammar_rules)

    # Realizar análisis sintáctico SLR
    if simulate_slr_parsing(tokens, actions, gotos):
        print("\nLa entrada es sintácticamente correcta.")
    else:
        print("Análisis completado con errores.")

# programmed by @melissaperez_
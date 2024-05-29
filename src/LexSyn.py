"""
LexSyn.py
Une el analizador léxico y sintáctico completo
"""

import sys
sys.path.insert(0, '/Users/melissa/Desktop/UVG/lenguajes/CC3071-LabAB/')

from lexicalAnalyzer.yalexParser import YALexParser
from lexicalAnalyzer.LexicalAnalyzer import *
from sintacticalAnalyzer.gammar import *
from sintacticalAnalyzer.parser import *

def main():
    # Definir la ruta del archivo de entrada
    file_path = './chars/Ejemplo1.txt'

    # Analizador Léxico
    lex_parser = YALexParser("./yalex/Ejemplo1.yal")
    lex_parser.parse()
    regex_tokens = lex_parser.generate_all_regex()  # Diccionario de definiciones de regex

    # Inicializar el analizador de gramática y cargar la gramática desde un archivo YAPar
    gram_parser = YAParParser('./yapar/Ejemplo1.yalp')
    gram_parser.parse()

    # Preparar el DFAUnion y generar los autómatas para cada token definido por regex
    dfa_union = DFAUnion()
    for token, regex in regex_tokens.items():
        dfa_transitions, start_state, accept_states = applyDirect(regex)
        draw_dfa(dfa_transitions, start_state, accept_states)
        os.rename('dfa_graph.png', f'dfa_graph_{token}.png')
        converted_transitions = convert_transitions(dfa_transitions)
        dfa_union.add_dfa(converted_transitions, start_state, accept_states, token)

    # Realizar la unión de DFAs
    afnd_transitions, afnd_start_state, afnd_accept_states, token_actions = dfa_union.union()
    draw_afnd(afnd_transitions, afnd_start_state, afnd_accept_states, token_actions)

    # Analizar archivo para obtener tokens
    tokens, lexical_errors = analizar_archivo(afnd_transitions, afnd_start_state, token_actions, file_path)
    
    if lexical_errors:
        print("Se encontraron errores léxicos:")
        for error in lexical_errors:
            print(f'Error léxico en línea {error[0]}, posición {error[1]}: {error[2]}')
        return

    # Añadir el token de fin de archivo a la lista de tokens para el análisis sintáctico
    tokens.append('$')
    print("LOS TOKENSSSSS:", tokens)

    # Inicializar el autómata LR(0) y construir la tabla de análisis sintáctico
    automata = AutomataLR0(gram_parser.grammar, gram_parser.tokens)
    automata.build_states()
    action_table, goto_table = automata.parsing_table()

    # Realizar análisis sintáctico SLR
    if simulate_slr_parsing(tokens, action_table, goto_table):
        print("Análisis completado con éxito. La entrada es sintácticamente correcta.")
    else:
        print("Análisis completado con errores.")

if __name__ == '__main__':
    main()

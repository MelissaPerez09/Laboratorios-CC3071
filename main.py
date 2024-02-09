"""
main.py
Uses all functionalities of classes
"""

from Parser import *
from ShuntingYard import *
from Thompson import *
from Subset import *
from MinAFD import *

expression = input("Enter the regular expression: ")
#chain = input("Enter the chain: ")

try:
    # Parse expression
    parsed_regex = parse_regex(expression)
    print(f"\nParsed expression: {parsed_regex}")

    # Shunting Yard
    shunting_yard = ShuntingYard(parsed_regex)
    postfix_expression = shunting_yard.shuntingYard()
    print(f"\nPostfix expression: {postfix_expression}")

    # McNaughton–Yamada–Thompson
    converter = Thompson()
    nfa = converter.convert2NFA(postfix_expression)
    converter.graph_nfa(nfa)
    nfa_symbols, nfa_states, nfa_transitions, nfa_start, nfa_end = converter.get_formatted_afn_params(nfa)
    # Thompson.process_input(chain, nfa)

    # Subsets
    afd = NFAtoAFDConverter(nfa_states, nfa_symbols, nfa_transitions, nfa_start, nfa_end)
    afd.convert_nfa_to_afd()
    afd.visualize_afd()

    # Min AFD
    # Get the AFD attributes from the afd converter
    afd_states, afd_symbols, afd_transitions, afd_start_state, afd_accept_states = (
        afd.afd_states,
        afd.afd_symbols,
        afd.afd_transitions,
        afd.afd_start_state,
        afd.afd_accept_states
    )
    minimized_afd = minimize_afd(afd_states, afd_symbols, afd_transitions, afd_start_state, afd_accept_states)
    new_states, new_symbols, new_transitions, new_start_state, new_accept_states = minimized_afd
    visualize_minimized_afd(new_states, new_symbols, new_transitions, new_start_state, new_accept_states)

except Exception as e:
    print(e)

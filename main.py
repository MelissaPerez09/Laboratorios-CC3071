"""
main.py
Uses all functionalities of classes
"""

from Parser import *
from ShuntingYard import *
from Thompson import *
from Subset import *
from MinAFD import *

expression = input("Enter the regular expression:\n  >>> ")
chain = input("Enter the chain:\n  >>> ")

try:
    # Parse expression
    parsed_regex = parse_regex(expression)
    print(f"\nParsed expression: {parsed_regex}")

    # Shunting Yard
    shunting_yard = ShuntingYard(parsed_regex)
    postfix_expression = shunting_yard.shuntingYard()
    print(f"Postfix expression: {postfix_expression}")

    # McNaughton–Yamada–Thompson
    converter = Thompson()
    nfa = converter.convert2NFA(postfix_expression)
    converter.graph_nfa(nfa)
    print("\n--NFA--\nSuccessfully graphed in 'nfa.png'")
    nfa_symbols, nfa_states, nfa_transitions, nfa_start, nfa_end = converter.get_formatted_afn_params(nfa)
    is_accepted = converter.simulate_nfa(nfa, chain)
    print(f"Chain '{chain}' is accepted: {is_accepted}")

    # Subsets
    afd = NFAtoAFDConverter(nfa_states, nfa_symbols, nfa_transitions, nfa_start, nfa_end)
    afd.convert_nfa_to_afd()
    afd.visualize_afd()
    print("\n--DFA--\nSuccessfully graphed in 'afd_fromAFN.png'")
    is_accepted2 = afd.simulate_dfa(chain)
    print(f"Chain '{chain}' is accepted: {is_accepted2}")

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
    print("\n--Min DFA--\nSuccessfully graphed in 'minimized_afd.png'")
    is_accepted3 = minimized_afd.simulate_minafd(chain)
    print(f"Chain '{chain}' is accepted: {is_accepted3}")

except Exception as e:
    print(e)

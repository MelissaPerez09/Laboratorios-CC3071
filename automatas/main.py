"""
main.py
Uses all functionalities of classes
"""

from Parser import *
from ShuntingYard import *
from Thompson import *
from Subset import *
from MinAFD import *
from DirectAFD import *

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
    afd = NFAtoAFDConverter(nfa_states, nfa_symbols, nfa_transitions, nfa_start, nfa_end)   # instancia de la clase NFAtoAFDConverter con los parametros de la clase Thompson
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
    ) # se obtienen los atributos de la clase afd
    minimized_afd = minimize_afd(afd_states, afd_symbols, afd_transitions, afd_start_state, afd_accept_states) 
    new_states, new_symbols, new_transitions, new_start_state, new_accept_states = minimized_afd # se obtienen los atributos de la clase minimize_afd
    visualize_minimized_afd(new_states, new_symbols, new_transitions, new_start_state, new_accept_states)
    print("\n--Min DFA--\nSuccessfully graphed in 'minimized_afd.png'")
    dfa_minimizer = DFAMinimizer(afd_states, afd_symbols, afd_transitions, afd_start_state, afd_accept_states)
    is_accepted3 = dfa_minimizer.simulate_minafd(chain)
    print(f"Chain '{chain}' is accepted: {is_accepted3}")
    
    # Direct AFD
    dfa_transitions, start_state, accept_states = applyDirect(expression)
    print("\n--Direct DFA--\nSuccessfully graphed in 'dfa_graph.png'")
    is_accepted4 = simulate_direct_afd(dfa_transitions, start_state, accept_states, chain)
    print(f"Chain '{chain}' is accepted: {is_accepted4}")
    

except Exception as e:
    print(e)

# programmed by @melissaperez_
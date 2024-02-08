"""
main.py
Uses all functionalities of classes
"""

from Parser import *
from ShuntingYard import *
from Thompson import *
from Subset import *

expression = input("Enter the regular expression: ")
#chain = input("Enter the chain: ")

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

#Thompson.process_input(chain, nfa)
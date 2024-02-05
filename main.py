"""
main.py
Uses all functionalities of classes
"""
from ShuntingYard import *
from Thompson import *

epsilon = "ε"
expression = input("Enter the regular expression: ")
#chain = input("Enter the chain: ")

shunting_yard = ShuntingYard(expression)
postfix_expression = shunting_yard.shuntingYard()
print(f"\nPostfix expression: {postfix_expression}")

converter = Thompson(epsilon)
nfa = converter.convert2NFA(postfix_expression)
converter.graph_nfa(nfa)

#Thompson.process_input(chain, nfa)
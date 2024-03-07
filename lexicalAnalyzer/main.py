"""
main.py
Uses all functionalities of classes for the Lexical Analyzer
"""

"""
from app import *
import tkinter as tk

root = tk.Tk()
app = LexicalAnalyzerApp(root)
root.mainloop()
"""

import sys
import os
sys.path.insert(0, '/Users/melissa/Desktop/UVG/lenguajes/CC3071-LabAB/')

from automatas.DirectAFD import *
from lexicalAnalyzer.yalexParser import YALexParser
from lexicalAnalyzer.finalAutomata import *

parser = YALexParser('./yalex/slr-1.yal')
parser.parse()
print(parser.generate_all_regex())

tokens = parser.generate_all_regex()

dfa_union = DFAUnion()

def convert_transitions(dfa_transitions):
    converted_transitions = {}
    for (state_frozenset, symbol), next_state_frozenset in dfa_transitions.items():
        state_str = str(state_frozenset)
        next_state_str = str(next_state_frozenset)
        
        if state_str not in converted_transitions:
            converted_transitions[state_str] = {}
        
        if symbol not in converted_transitions[state_str]:
            converted_transitions[state_str][symbol] = set()
        
        converted_transitions[state_str][symbol].add(next_state_str)
    
    return converted_transitions

for token, regex in tokens.items():
    dfa_transitions, start_state, accept_states = applyDirect(regex)
    draw_dfa(dfa_transitions, start_state, accept_states)
    os.rename('dfa_graph.png', f'dfa_graph_{token}.png')
    
    converted_transitions = convert_transitions(dfa_transitions)
    dfa_union.add_dfa(converted_transitions, start_state, accept_states)

afnd_transitions, afnd_start_state, afnd_accept_states = dfa_union.union()
draw_afnd(afnd_transitions, afnd_start_state, afnd_accept_states)

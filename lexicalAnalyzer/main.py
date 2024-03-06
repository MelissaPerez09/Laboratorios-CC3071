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
from yalexParser import YALexParser

parser = YALexParser('./yalex/slr-3.yal')
parser.parse()
print(parser.generate_all_regex())

tokens = parser.generate_all_regex()

parsed_regex_dict = {}
for token, regex in tokens.items():
    dfa_transitions, start_state, accept_states = applyDirect(regex)
    draw_dfa(dfa_transitions, start_state, accept_states)
    os.rename('dfa_graph.png', f'dfa_graph_{token}.png')

"""
app.py
Lexical Analyzer App
"""

import sys
sys.path.insert(0, '/Users/melissa/Desktop/UVG/lenguajes/CC3071-LabAB/')

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import os
from automatas.DirectAFD import *
from lexicalAnalyzer.yalexParser import YALexParser
from lexicalAnalyzer.finalAutomata import *

class LexicalAnalyzerApp:
    """
    Constructor
    :param root: Root
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Lexical Analyzer App")

        self.open_button = ttk.Button(root, text="Open file", command=self.open_file)
        self.open_button.pack()
        
        self.text_area = ScrolledText(root, wrap=tk.WORD, width=125, height=25)
        self.text_area.pack(expand=True, fill=tk.BOTH)

        self.analysis_button = ttk.Button(root, text="Analyze", command=self.analyze_and_draw)
        self.analysis_button.pack()

        self.output_terminal = ScrolledText(root, wrap=tk.WORD, width=125, height=25)
        self.output_terminal.pack(expand=True, fill=tk.BOTH)
        
        self.save_button = ttk.Button(root, text="Save file", command=self.save_file)
        self.save_button.pack()

    """
    Open file
    """
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("YALex Files", "*.yal")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert(tk.END, content)
        file_name = os.path.basename(file_path)
        self.output_terminal.insert(tk.END, f"\n>-----------------------------------\n{file_name} opened correctly\n------------------------------------\n")
    
    """
    Save file
    """
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".yalex", filetypes=[("YALex Files", "*.yal")])
        if file_path:
            with open(file_path, 'w') as file:
                content = self.text_area.get('1.0', tk.END)
                file.write(content)

    """
    Analyze and draw
    reads the content of the text area, parses the YALex file, generates the regex for all the tokens,
    returns the regex for all the tokens and draws the DFA and AFND
    """
    def analyze_and_draw(self):
        self.output_terminal.insert(tk.END, "\n>-----------------------------------\nReading and analyzing the file...\n------------------------------------\n")
        content = self.text_area.get('1.0', tk.END)
        with open('temp.yal', 'w') as temp_file:
            temp_file.write(content)

        parser = YALexParser('temp.yal')
        parser.parse()
        tokens = parser.generate_all_regex()

        dfa_union = DFAUnion()

        """
        Convert transitions
        :param dfa_transitions: DFA transitions
        returns the converted transitions
        """
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
            dfa_union.add_dfa(converted_transitions, start_state, accept_states, token)

        afnd_transitions, afnd_start_state, afnd_accept_states, token_actions = dfa_union.union()
        draw_afnd(afnd_transitions, afnd_start_state, afnd_accept_states, token_actions)
        generated = "\nGenerated afnd.png\n"
        self.output_terminal.insert(tk.END, generated)

        result_text = "\n".join([f"token_action: {token} -> regex: {regex}" for token, regex in tokens.items()])
        self.output_terminal.insert(tk.END, f"\n>-----------------------------------\nAnalyzed tokens:\n{result_text}\n------------------------------------\n-----------------------------------<\n")

        os.remove('temp.yal')

# programmed by @melissaperez_
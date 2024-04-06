"""
app.py
Lexical Analyzer App
"""

import sys
sys.path.insert(0, '/Users/melissa/Desktop/UVG/lenguajes/CC3071-LabAB/')

import tkinter as tk
from tkinter import filedialog, messagebox, Menu
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import os
from automatas.DirectAFD import *
from lexicalAnalyzer.yalexParser import YALexParser
from lexicalAnalyzer.finalAutomata import *
from lexicalAnalyzer.lexer import *
from lexicalAnalyzer.LexicalAnalyzer import *

class LexicalAnalyzerApp:
    """
    Constructor
    :param root: Root
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Lexical Analyzer App")
        
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        self.yalex_file_path = None
        self.txt_file_path = None

        self.lexical_analyzer_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Lexical Analyzer", menu=self.lexical_analyzer_menu)
        self.lexical_analyzer_menu.add_command(label="LA Generator", command=self.show_generator_ui)
        self.lexical_analyzer_menu.add_command(label="Analyzer", command=self.show_analyzer_ui)

        self.init_ui_elements()
    
    def init_ui_elements(self):
        # Botones y áreas de texto para el generador LA
        self.open_button_generator = ttk.Button(self.root, text="Open YALex file", command=self.open_YALexfile)
        self.generate_src_button = ttk.Button(self.root, text="Generate Source Code", command=self.generate_source_code_from_YALex)
        self.text_area_generator = ScrolledText(self.root, wrap=tk.WORD, width=125, height=25)
        self.output_terminal_generator = ScrolledText(self.root, wrap=tk.WORD, width=125, height=10)

        # Botones y áreas de texto para el analizador
        self.open_button_analyzer = ttk.Button(self.root, text="Open chars file", command=self.open_TXTfile)
        self.analyze_button = ttk.Button(self.root, text="Analyze", command=self.analyze)
        self.text_area_analyzer = ScrolledText(self.root, wrap=tk.WORD, width=125, height=25)
        self.output_terminal_analyzer = ScrolledText(self.root, wrap=tk.WORD, width=125, height=10)

        self.save_button = ttk.Button(self.root, text="Save file", command=self.save_file)
    
    def show_generator_ui(self):
        # Ocultar elementos de UI del analizador
        self.hide_analyzer_ui()

        # Mostrar elementos de UI del generador LA
        self.open_button_generator.pack()
        self.generate_src_button.pack()
        self.text_area_generator.pack(expand=True, fill=tk.BOTH)
        self.output_terminal_generator.pack(expand=True, fill=tk.BOTH) 

    def hide_generator_ui(self):
        # Ocultar elementos de UI del generador LA
        self.open_button_generator.pack_forget()
        self.generate_src_button.pack_forget()
        self.text_area_generator.pack_forget()
        self.output_terminal_generator.pack_forget() 
        

    def show_analyzer_ui(self):
        # Ocultar elementos de UI del generador LA
        self.hide_generator_ui()

        # Mostrar elementos de UI del analizador
        self.open_button_analyzer.pack()
        self.text_area_analyzer.pack(expand=True, fill=tk.BOTH)
        self.analyze_button.pack()
        self.output_terminal_analyzer.pack(expand=True, fill=tk.BOTH)
        self.save_button.pack()

    def hide_analyzer_ui(self):
        # Ocultar elementos de UI del analizador
        self.open_button_analyzer.pack_forget()
        self.text_area_analyzer.pack_forget()
        self.analyze_button.pack_forget()
        self.output_terminal_analyzer.pack_forget()
        self.save_button.pack_forget()

    """
    Open file
    """
    def open_YALexfile(self):
        self.yalex_file_path = filedialog.askopenfilename(filetypes=[("YALex Files", "*.yal")])
        if self.yalex_file_path:
            with open(self.yalex_file_path, 'r') as file:
                content = file.read()
                self.text_area_generator.delete('1.0', tk.END)
                self.text_area_generator.insert(tk.END, content)
            file_name = os.path.basename(self.yalex_file_path)
            self.output_terminal_generator.insert(tk.END, f"\n>-----------------------------------\n{file_name} opened correctly\n------------------------------------\n")
        
    def open_TXTfile(self):
        self.txt_file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if self.txt_file_path:
            with open(self.txt_file_path, 'r') as file:
                content = file.read()
                self.text_area_analyzer.delete('1.0', tk.END)
                self.text_area_analyzer.insert(tk.END, content)
            file_name = os.path.basename(self.txt_file_path)
            self.output_terminal_analyzer.insert(tk.END, f"\n>-----------------------------------\n{file_name} opened correctly\n------------------------------------\n")
    
    """
    Save file
    """
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                content = self.text_area_analyzer.get('1.0', tk.END)
                file.write(content)

    """
    Generate Source Code
    """
    def generate_source_code_from_YALex(self):
        if self.yalex_file_path:
            output_path = './lexicalAnalyzer/LexicalAnalyzer.py'
            try:
                generate_source_code(self.yalex_file_path, output_path)

                self.output_terminal_generator.insert(tk.END, "\n>-----------------------------------\n")
                self.output_terminal_generator.insert(tk.END, "Source code generated successfully at:\n")
                self.output_terminal_generator.insert(tk.END, output_path)
                self.output_terminal_generator.insert(tk.END, "\n------------------------------------\n")
                return output_path
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                self.output_terminal_generator.insert(tk.END, f"\n>-----------------------------------\nAn error occurred: {e}\n------------------------------------\n")
        else:
            messagebox.showinfo("Info", "Please open a YALex file first.")
            return None
    
    """
    Use Lexical Analyzer
    """
    def analyze(self, source_code_path=None):
        if source_code_path or self.txt_file_path:
            try:
                if source_code_path:
                    with open(source_code_path, 'r') as file:
                        texto_entrada = file.read().strip()
                else:
                    with open(self.txt_file_path, 'r') as file:
                        texto_entrada = file.read().strip()
                tokens, errores = analizar_archivo(afnd_transitions, afnd_start_state, token_actions, texto_entrada)
                
                resultado = ""
                if tokens:
                    resultado += 'Tokens:\n' + '\n'.join(map(str, tokens)) + '\n'
                else:
                    resultado += 'No se encontró un token válido para la cadena de entrada.'
                
                erroresF = ""
                if errores:
                    for error in errores:
                        erroresF += f'\nError léxico en la línea {error[0]}, posición {error[1]}: {error[2]}'
                else:
                    erroresF += '\nNo se encontraron errores.'

                self.output_terminal_analyzer.insert(tk.END, "\n>-----------------------------------\n")
                self.output_terminal_analyzer.insert(tk.END, resultado)
                self.output_terminal_analyzer.insert(tk.END, erroresF)
                self.output_terminal_analyzer.insert(tk.END, "\n------------------------------------\n")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                self.output_terminal_analyzer.insert(tk.END, f"\n>-----------------------------------\nAn error occurred: {e}\n------------------------------------\n")
        else:
            messagebox.showinfo("Info", "Please open a text file to analyze.")


    """
    Analyze and draw
    reads the content of the text area, parses the YALex file, generates the regex for all the tokens,
    returns the regex for all the tokens and draws the DFA and AFND
    """
    def analyze_and_draw(self):
        self.output_terminal_generator.insert(tk.END, "\n>-----------------------------------\nReading and analyzing the file...\n------------------------------------\n")
        content = self.text_area_generator.get('1.0', tk.END)
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
        self.output_terminal_generator.insert(tk.END, generated)

        result_text = "\n".join([f"token_action: {token} -> regex: {regex}" for token, regex in tokens.items()])
        self.output_terminal_generator.insert(tk.END, f"\n>-----------------------------------\nAnalyzed tokens:\n{result_text}\n------------------------------------\n-----------------------------------<\n")

        os.remove('temp.yal')

# programmed by @melissaperez_
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
        self.text_area_generator = ScrolledText(self.root, wrap=tk.WORD, width=125, height=30)
        self.output_terminal_generator = ScrolledText(self.root, wrap=tk.WORD, width=125, height=15)
        self.save_button_generator = ttk.Button(self.root, text="Save file", command=self.save_file_generator)

        # Botones y áreas de texto para el analizador
        self.open_button_analyzer = ttk.Button(self.root, text="Open chars file", command=self.open_TXTfile)
        self.analyze_button = ttk.Button(self.root, text="Analyze", command=self.analyze)
        self.text_area_analyzer = ScrolledText(self.root, wrap=tk.WORD, width=125, height=15)
        self.output_terminal_analyzer = ScrolledText(self.root, wrap=tk.WORD, width=125, height=30)
        self.save_button_analyzer = ttk.Button(self.root, text="Save file", command=self.save_file_analyzer)
    
    def show_generator_ui(self):
        # Ocultar elementos de UI del analizador
        self.hide_analyzer_ui()

        # Mostrar elementos de UI del generador LA
        self.open_button_generator.pack()
        self.text_area_generator.pack(expand=True, fill=tk.BOTH)
        self.generate_src_button.pack()
        self.output_terminal_generator.pack(expand=True, fill=tk.BOTH) 
        self.save_button_generator.pack()

    def hide_generator_ui(self):
        # Ocultar elementos de UI del generador LA
        self.open_button_generator.pack_forget()
        self.generate_src_button.pack_forget()
        self.text_area_generator.pack_forget()
        self.output_terminal_generator.pack_forget() 
        self.save_button_generator.pack_forget()
        

    def show_analyzer_ui(self):
        # Ocultar elementos de UI del generador LA
        self.hide_generator_ui()

        # Mostrar elementos de UI del analizador
        self.open_button_analyzer.pack()
        self.text_area_analyzer.pack(expand=True, fill=tk.BOTH)
        self.analyze_button.pack()
        self.output_terminal_analyzer.pack(expand=True, fill=tk.BOTH)
        self.save_button_analyzer.pack()

    def hide_analyzer_ui(self):
        # Ocultar elementos de UI del analizador
        self.open_button_analyzer.pack_forget()
        self.text_area_analyzer.pack_forget()
        self.analyze_button.pack_forget()
        self.output_terminal_analyzer.pack_forget()
        self.save_button_analyzer.pack_forget()

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
    def save_file_generator(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".yal", filetypes=[("YALex Files", "*.yal")])
        if file_path:
            with open(file_path, 'w') as file:
                content = self.text_area_generator.get('1.0', tk.END)
                file.write(content)
                
    def save_file_analyzer(self):
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

# programmed by @melissaperez_
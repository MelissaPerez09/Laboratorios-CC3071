"""
app.py
Sintactial Analyzer App
"""

import sys
sys.path.insert(0, '/Users/melissa/Desktop/UVG/lenguajes/CC3071-LabAB/')

from lexicalAnalyzer.yalexParser import *
from sintacticalAnalyzer.gammarUI import *
from sintacticalAnalyzer.functions import *

import tkinter as tk
from tkinter import filedialog, Text

root = tk.Tk()
root.title("Sintactical Analyzer Generator")

# Funciones para abrir y guardar archivos
def open_file(editor, filetypes):
    filepath = filedialog.askopenfilename(filetypes=filetypes)
    if filepath:
        with open(filepath, 'r') as file:
            content = file.read()
            editor.delete('1.0', tk.END)
            editor.insert(tk.END, content)
        editor.filepath = filepath

def save_as_file(editor, default_extension):
    filetypes = [(f"{default_extension.upper()} Files", f"*.{default_extension}")]
    filepath = filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=f".{default_extension}")
    if filepath:
        content = editor.get('1.0', tk.END)
        with open(filepath, 'w') as file:
            file.write(content)
        editor.filepath = filepath

# Función para imprimir en la consola
def print_to_console(msg):
    console.insert(tk.END, msg + '\n')
    console.see(tk.END)

old_print = print
def print(*args, **kwargs):
    old_print(*args, **kwargs)
    msg = ' '.join(map(str, args))
    print_to_console(msg)

# Función para generar el análisis
def generate_analysis():
    # Uso de los parsers
    if hasattr(editor_yalex, 'filepath') and editor_yalex.filepath and hasattr(editor_yapar, 'filepath') and editor_yapar.filepath:
        yapar_parser = YAParParser(editor_yapar.filepath)
        yapar_parser.parse()

        yalex_parser = YALexParser(editor_yalex.filepath)
        yalex_parser.parse()
        yalex_tokens = yalex_parser.generate_all_regex()

        print("********************************")
        
        # Validación de tokens y generación de autómatas
        is_valid, missing_tokens = validate_tokens(yapar_parser.tokens, yalex_tokens)
        if not is_valid:
            print(f"Token validation: False\n(!)Error, Tokens missing: {missing_tokens}")
            print("--------------------------------")
        else:
            print("Token validation: True")
            
            print("\nDetected grammar:")
            for nonterminal, productions in yapar_parser.grammar.items():
                print(f"{nonterminal} -> {[' '.join(prod) for prod in productions]}")
            
            automata = AutomataLR0(yapar_parser.grammar, yapar_parser.tokens)
            automata.build_states()
            automata.parsing_actions()
            
            state_to_index = {tuple(state): index for index, state in enumerate(automata.states)}

            generate_automata_graph(automata, 'automataLR(0)', state_to_index)

            # Calcular y mostrar los conjuntos FIRST y FOLLOW
            first_sets, follow_sets = compute_sets(yapar_parser.grammar)
            print("\nFIRST sets:", first_sets)
            print("\nFOLLOW sets:", follow_sets)

            print("\nAutomata generated successfully!")
            print("--------------------------------")
    else:
        print("Please load both YALex and YAPar files before generating analysis.")

# Frames para los editores de texto
frame_yalex = tk.Frame(root)
frame_yalex.grid(row=1, column=0, padx=10, pady=10)

frame_yapar = tk.Frame(root)
frame_yapar.grid(row=1, column=1, padx=10, pady=10)

# Editores de texto
editor_yalex = Text(frame_yalex, height=20, width=60)
editor_yalex.pack()
editor_yalex.filepath = None

editor_yapar = Text(frame_yapar, height=20, width=60)
editor_yapar.pack()
editor_yapar.filepath = None

# Botones para abrir los archivos
button_open_yalex = tk.Button(root, text="Open YALex", command=lambda: open_file(editor_yalex, [('YALex Files', '*.yal')]))
button_open_yalex.grid(row=0, column=0, padx=10, pady=10)

button_open_yapar = tk.Button(root, text="Open YAPar", command=lambda: open_file(editor_yapar, [('YAPar Files', '*.yalp')]))
button_open_yapar.grid(row=0, column=1, padx=10, pady=10)

# Botones para guardar los archivos
button_saveas_yalex = tk.Button(frame_yalex, text="Save As", command=lambda: save_as_file(editor_yalex, 'yal'))
button_saveas_yalex.pack()

button_saveas_yapar = tk.Button(frame_yapar, text="Save As", command=lambda: save_as_file(editor_yapar, 'yalp'))
button_saveas_yapar.pack()

# Botón para generar el analizador
button_generate = tk.Button(root, text="Generate", command=generate_analysis, width=20)
button_generate.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Consola de salida
console_frame = tk.Frame(root)
console_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

console = Text(console_frame, height=10, width=100)
console.pack()

root.mainloop()

# programmed by @melissaperez_
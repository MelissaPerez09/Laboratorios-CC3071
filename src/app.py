"""
app.py
Lexical and Sintactial Analyzer App
"""

import sys
import tkinter as tk
from tkinter import filedialog, Text
sys.path.insert(0, '/Users/melissa/Desktop/UVG/lenguajes/CC3071-LabAB/')

from src.LexSyn import *

class DualRedirector(object):
    def __init__(self, widget):
        self.widget = widget
        self.standard_out = sys.stdout

    def write(self, str):
        self.widget.insert(tk.END, str)
        self.widget.see(tk.END)
        self.standard_out.write(str)

    def flush(self):
        pass

root = tk.Tk()
root.title("Sintactical Analyzer")

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

# Función para el análisis
def analyze():
    LexSyn(editor_yalex.filepath, editor_yapar.filepath, editor_chars.filepath)


# Editor de texto para yalex
frame_yalex = tk.Frame(root)
frame_yalex.grid(row=1, column=0, padx=10, pady=10)
editor_yalex = Text(frame_yalex, height=15, width=58)
editor_yalex.pack()
editor_yalex.filepath = None

# Botones para yalex
button_open_yalex = tk.Button(frame_yalex, text="Open YALex", command=lambda: open_file(editor_yalex, [('YALex Files', '*.yal')]))
button_open_yalex.pack(side=tk.LEFT, padx=10)
button_saveas_yalex = tk.Button(frame_yalex, text="Save YALex", command=lambda: save_as_file(editor_yalex, 'yal'))
button_saveas_yalex.pack(side=tk.RIGHT, padx=10)

# Editor de texto para yapar
frame_yapar = tk.Frame(root)
frame_yapar.grid(row=1, column=1, padx=10, pady=10)
editor_yapar = Text(frame_yapar, height=15, width=58)
editor_yapar.pack()
editor_yapar.filepath = None

# Botones para yapar
button_open_yapar = tk.Button(frame_yapar, text="Open YAPar", command=lambda: open_file(editor_yapar, [('YAPar Files', '*.yalp')]))
button_open_yapar.pack(side=tk.LEFT, padx=10)
button_saveas_yapar = tk.Button(frame_yapar, text="Save YAPar", command=lambda: save_as_file(editor_yapar, 'yalp'))
button_saveas_yapar.pack(side=tk.RIGHT, padx=10)

# Editor de texto para los caracteres
frame_chars = tk.Frame(root)
frame_chars.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
editor_chars = Text(frame_chars, height=10, width=120)
editor_chars.pack()
editor_chars.filepath = None

# Botones para chars
button_open_chars = tk.Button(frame_chars, text="Open Chars", command=lambda: open_file(editor_chars, [('Text Files', '*.txt')]))
button_open_chars.pack(side=tk.LEFT, padx=10)

button_saveas_chars = tk.Button(frame_chars, text="Save Chars", command=lambda: save_as_file(editor_chars, 'txt'))
button_saveas_chars.pack(side=tk.RIGHT, padx=10)

# Botón para analizar
button_generate = tk.Button(root, text="ANALYZE", command=analyze, width=20)
button_generate.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Consola de salida
console_frame = tk.Frame(root)
console_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

console = Text(console_frame, height=15, width=120)
console.pack()

sys.stdout = DualRedirector(console)

root.mainloop()

# programmed by @melissaperez_
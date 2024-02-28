"""
app.py
Lexical Analyzer App
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk

class LexicalAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lexical Analyzer App")

        self.open_button = ttk.Button(root, text="Open file", command=self.open_file)
        self.open_button.pack()
        
        self.text_area = ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.text_area.pack(expand=True, fill=tk.BOTH)

        self.analysis_button = ttk.Button(root, text="Analyze", command=self.analyze)
        self.analysis_button.pack()

        self.output_terminal = ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.output_terminal.pack(expand=True, fill=tk.BOTH)
        
        self.save_button = ttk.Button(root, text="Save file", command=self.save_file)
        self.save_button.pack()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("YALex Files", "*.yal")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert(tk.END, content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".yalex", filetypes=[("YALex Files", "*.yal")])
        if file_path:
            with open(file_path, 'w') as file:
                content = self.text_area.get('1.0', tk.END)
                file.write(content)

    def exit_app(self):
        self.root.quit()

    def analyze(self):
        pass

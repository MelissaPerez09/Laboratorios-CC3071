"""
main.py
Uses all functionalities of classes for the Lexical Analyzer
"""

from app import *
import tkinter as tk

"""
Main function
Creates the GUI
"""
if __name__ == "__main__":
    root = tk.Tk()
    app = LexicalAnalyzerApp(root)
    root.mainloop()
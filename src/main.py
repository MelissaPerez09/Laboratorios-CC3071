"""
main.py
Lexical and syntactical analyzer main, no UI
"""
import sys
sys.path.insert(0, '/Users/melissa/Desktop/UVG/lenguajes/CC3071-LabAB/')

from src.LexSyn import *

yalex_path = './yalex/Ejemplo1.yal'
yapar_path = './yapar/Ejemplo1.yalp'
chars_path = './chars/Ejemplo1.txt'

LexSyn(yalex_path, yapar_path, chars_path)